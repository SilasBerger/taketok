use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};
use tauri::State;
use crate::error::TakeTokError;
use crate::models::{ImportResponse, SourceUrl};
use crate::path_utils::taketok_home;
use crate::schema;
use crate::state::TakeTokState;

#[tauri::command]
pub fn fetch_source_urls() -> Result<Vec<SourceUrl>, TakeTokError> {
    let db_path = taketok_home().join("data").join("dev.sqlite");
    let db_path_str = db_path.to_str().unwrap();
    let mut connection = SqliteConnection::establish(db_path_str)?;

    let result = schema::source_url::dsl::source_url
        .select(SourceUrl::as_select())
        .load(&mut connection)?;

    Ok(result)
}

#[tauri::command]
pub async fn request_a_transcript(state: State<'_, TakeTokState>, video_id: String) -> Result<String, TakeTokError> {
    let video_output_dir = &state.config.video_output_dir;
    let whisper_model = &state.config.whisper_model;
    let result = state
        .core_api_client
        .request_transcript(&video_id, video_output_dir, whisper_model)
        .await?;
    Ok(result)
}

#[tauri::command]
pub async fn import_from_source_url(source_url: String, state: State<'_, TakeTokState>) -> Result<ImportResponse, TakeTokError> {
    let video_output_dir = &state.config.video_output_dir;
    println!("{}", video_output_dir);
    let result = state
        .core_api_client
        .import_from_source_url(&source_url, &video_output_dir)
        .await?;
    Ok(result)
}
