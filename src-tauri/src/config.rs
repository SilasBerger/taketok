use std::path::PathBuf;
use serde::{Deserialize, Serialize};
use crate::error::TakeTokError;
use crate::utils::read_as_json;

#[derive(Serialize, Deserialize, Debug)]
pub struct Config {
    #[serde(rename = "whisperModel")]
    pub whisper_model: String,
}

impl Config {
    pub fn load(config_path: PathBuf) -> Result<Self, TakeTokError> {
        read_as_json(&config_path)
    }
}