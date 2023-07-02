// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod path_utils;
mod models;
mod schema;

use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};
use crate::models::{SourceUrl, TranscriptRequest, TranscriptResponse};
use crate::path_utils::taketok_home;
use crate::schema::source_url::dsl::source_url;

#[tauri::command]
fn fetch_source_urls() -> Vec<SourceUrl> {
    let db_path = taketok_home().join("data").join("dev.sqlite");
    let db_path_str = db_path.to_str().unwrap();
    let mut connection = SqliteConnection::establish(db_path_str)
        .unwrap_or_else(|_| panic!("Error connecting to {}", db_path_str));

    let result = source_url
        .select(SourceUrl::as_select())
        .load(&mut connection)
        .unwrap();

    result
}

#[tauri::command]
fn request_a_transcript() -> String {
    let client = reqwest::blocking::Client::new();

    let request_body = TranscriptRequest {
        video_id: "7193720678988746026".to_string(),
        video_output_dir: "/Users/silas/taketok/videos/dev".to_string(),
        whisper_model: "small".to_string(),
    };

    let result = client
        .post("http://127.0.0.1:5000/transcribe")
        .json(&request_body)
        .send()
        .unwrap();

    let transcript_response: TranscriptResponse = result.json().unwrap();
    transcript_response.transcript.to_string()
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
