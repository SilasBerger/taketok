// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};

use crate::commands::{fetch_source_urls, request_a_transcript};
use crate::core_api_client::CoreApiClient;
use crate::state::TakeTokState;

mod path_utils;
mod models;
mod schema;
mod error;
mod core_api_client;
mod commands;
mod state;

fn main() {
    let api_client = CoreApiClient::mock();
    let state = TakeTokState {
        core_api_client: api_client,
    };

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            fetch_source_urls,
            request_a_transcript
        ])
        .manage(state)
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
