// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod path_utils;
mod dao;
mod schema;

use diesel::{Connection, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection};
use crate::dao::{SourceUrl};
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

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![fetch_source_urls])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
