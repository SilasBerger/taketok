// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use diesel::{QueryDsl, SelectableHelper, SqliteConnection};

use crate::commands::{fetch_source_urls, request_a_transcript, import_from_source_url};
use crate::config::Config;
use crate::core_api_client::CoreApiClient;
use crate::path_utils::{config_file, taketok_home};
use crate::state::TakeTokState;

mod path_utils;
mod models;
mod schema;
mod error;
mod core_api_client;
mod commands;
mod state;
mod config;

fn main() {
    let config = Config::load(config_file("default"))
        .expect("Unable to load config 'default'");

    let core_api_client = CoreApiClient::new();

    let state = TakeTokState {
        core_api_client,
        config
    };

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            fetch_source_urls,
            request_a_transcript,
            import_from_source_url,
        ])
        .manage(state)
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
