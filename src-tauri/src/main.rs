// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::ops::Mul;
use std::time::Duration;

use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};

use crate::core_api_client::{CoreApiClient};
use crate::error::TakeTokError;
use crate::models::{SourceUrl, TranscriptRequest, TranscriptResponse};
use crate::path_utils::taketok_home;
use crate::schema::source_url::dsl::source_url;

mod path_utils;
mod models;
mod schema;
mod error;
mod core_api_client;

#[tauri::command]
fn fetch_source_urls() -> Result<Vec<SourceUrl>, TakeTokError> {
    let db_path = taketok_home().join("data").join("dev.sqlite");
    let db_path_str = db_path.to_str().unwrap();
    let mut connection = SqliteConnection::establish(db_path_str)?;

    let result = source_url
        .select(SourceUrl::as_select())
        .load(&mut connection)?;

    Ok(result)
}

#[tauri::command]
async fn request_a_transcript() -> Result<String, TakeTokError> {
    let api_client = CoreApiClient::mock();
    Ok(api_client.request_transcript().await?)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            fetch_source_urls,
            request_a_transcript
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
