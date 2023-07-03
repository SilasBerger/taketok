use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};
use crate::core_api_client::CoreApiClient;
use crate::error::TakeTokError;
use crate::models::SourceUrl;
use crate::path_utils::taketok_home;
use crate::schema::source_url::dsl::source_url;

#[tauri::command]
pub fn fetch_source_urls() -> Result<Vec<SourceUrl>, TakeTokError> {
    let db_path = taketok_home().join("data").join("dev.sqlite");
    let db_path_str = db_path.to_str().unwrap();
    let mut connection = SqliteConnection::establish(db_path_str)?;

    let result = source_url
        .select(SourceUrl::as_select())
        .load(&mut connection)?;

    Ok(result)
}

#[tauri::command]
pub async fn request_a_transcript() -> Result<String, TakeTokError> {
    let api_client = CoreApiClient::mock();
    Ok(api_client.request_transcript().await?)
}
