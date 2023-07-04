use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use serde::de::DeserializeOwned;
use crate::error::TakeTokError;

pub fn read_as_json<T: DeserializeOwned>(path: &PathBuf) -> Result<T, TakeTokError>{
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    Ok(serde_json::from_reader(reader)?)
}