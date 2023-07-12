use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper};
use tauri::{AppHandle, Manager, State, Wry};
use crate::db::repository::{insert_author_if_not_exists, insert_challenges, insert_hashtags, insert_transcript, load_all_video_data, mark_source_as_processed, save_video_metadata, update_author_info_if_changed};
use crate::db::db_models::SourceUrl;
use crate::error::TakeTokError;
use crate::db::schema;
use crate::models::VideoFullInfo;
use crate::state::TakeTokState;
use crate::utils::connect_to_db;

#[tauri::command]
pub fn fetch_source_urls() -> Result<Vec<SourceUrl>, TakeTokError> {
    let mut db_connection = connect_to_db("default")?;
    let result = schema::source_url::dsl::source_url
        .select(SourceUrl::as_select())
        .load(&mut db_connection)?;

    Ok(result)
}

#[tauri::command]
pub async fn request_transcript(state: State<'_, TakeTokState>, video_id: String) -> Result<String, TakeTokError> {
    let whisper_model = &state.config.whisper_model;
    let result = state
        .core_api_client
        .request_transcript(&video_id, "default", whisper_model) // TODO: Fix hard-coded config name.
        .await?;
    Ok(result)
}

#[tauri::command]
pub async fn import_from_source_url(source_url: String, state: State<'_, TakeTokState>) -> Result<(), TakeTokError> {
    let mut db_connection = connect_to_db("default")?;

    let import_response = state
        .core_api_client
        .import_from_source_url(&source_url, "default")
        .await?;

    let video = import_response.video;
    let video_id = &video.id;
    let author = import_response.author;
    let author_id = &author.id;

    // TODO: Consider aborting if video ID exists
    db_connection.transaction::<(), TakeTokError, _>(| mut conn| {
        insert_author_if_not_exists(&mut conn, author_id)?;
        update_author_info_if_changed(&mut conn, &author)?;
        save_video_metadata(&mut conn, &video, &author.id)?;
        insert_hashtags(&mut conn, video_id, &video.hashtags)?;
        insert_challenges(&mut conn, video_id, &video.challenges)?;
        mark_source_as_processed(&mut conn, &source_url)?;
        Ok(())
    })?;

    let transcript = state
        .core_api_client
        .request_transcript(video_id, "default", &state.config.whisper_model) // TODO: Fix hard-coded config name.
        .await?;

    db_connection.transaction::<(), TakeTokError, _>(| mut conn| {
        insert_transcript(&mut conn, video_id, &transcript)?;
        Ok(())
    })?;

    Ok(())
}

#[tauri::command]
pub async fn toggle_devtools(app: AppHandle<Wry>) -> Result<(), TakeTokError> {
    if let Some(window) = app.get_window("main") {
        if window.is_devtools_open() {
            window.close_devtools();
        } else {
            window.open_devtools();
        }
    }
    Ok(())
}

#[tauri::command]
pub async fn get_all_video_data() -> Result<Vec<VideoFullInfo>, TakeTokError> {
    let mut db_connection = connect_to_db("default")?;
    load_all_video_data(&mut db_connection)
}