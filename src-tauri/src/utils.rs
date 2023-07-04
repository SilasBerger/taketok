use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use diesel::{Connection, SqliteConnection};
use serde::de::DeserializeOwned;
use crate::error::TakeTokError;
use crate::path_utils::taketok_home;

pub fn read_as_json<T: DeserializeOwned>(path: &PathBuf) -> Result<T, TakeTokError>{
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    Ok(serde_json::from_reader(reader)?)
}

pub fn connect_to_db(db_name: &str) -> Result<SqliteConnection, TakeTokError> {
    let db_file_name = format!("{}.sqlite", db_name);
    let db_path = taketok_home().join("data").join(&db_file_name);
    Ok(SqliteConnection::establish(db_path.to_str().unwrap())?)
}