// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};

use crate::commands::{fetch_source_urls, request_a_transcript};

mod path_utils;
mod models;
mod schema;
mod error;
mod core_api_client;
mod commands;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            fetch_source_urls,
            request_a_transcript
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
