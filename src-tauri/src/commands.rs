use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};
use tauri::State;
use crate::dao::insert_author_if_not_exists;
use crate::error::TakeTokError;
use crate::models::{ImportResponse, SourceUrl};
use crate::path_utils::taketok_home;
use crate::schema;
use crate::state::TakeTokState;
use crate::utils::connect_to_db;

#[tauri::command]
pub fn fetch_source_urls() -> Result<Vec<SourceUrl>, TakeTokError> {
    let mut db_connection = connect_to_db("dev")?;
    let result = schema::source_url::dsl::source_url
        .select(SourceUrl::as_select())
        .load(&mut db_connection)?;

    Ok(result)
}

#[tauri::command]
pub async fn request_transcript(state: State<'_, TakeTokState>, video_id: String) -> Result<String, TakeTokError> {
    let video_output_dir = &state.config.video_output_dir;
    let whisper_model = &state.config.whisper_model;
    let result = state
        .core_api_client
        .request_transcript(&video_id, video_output_dir, whisper_model)
        .await?;
    Ok(result)
}

#[tauri::command]
pub async fn import_from_source_url(source_url: String, state: State<'_, TakeTokState>) -> Result<(), TakeTokError> {
    let video_output_dir = &state.config.video_output_dir;
    let mut db_connection = connect_to_db("dev")?;

    let import_response = state
        .core_api_client
        .import_from_source_url(&source_url, &video_output_dir)
        .await?;

    let video = import_response.video;
    let video_id = &video.id;
    let author = import_response.author;
    let author_id = &author.id;

    db_connection.transaction::<(), TakeTokError, _>(| mut conn| {
        insert_author_if_not_exists(&mut conn, author_id)?;
        Ok(())
    })?;

    /*
    As transaction:
    - save author if not exists
    - update author info if changed
    - save video metadata
    - insert hashtags
    - insert challenges
    (- mark source URL as processed)
     */

    Ok(())
}
