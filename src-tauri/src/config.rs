use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use serde::{Deserialize, Serialize};
use crate::error::TakeTokError;

#[derive(Serialize, Deserialize, Debug)]
pub struct Config {
    #[serde(rename = "videoOutputDir")]
    pub video_output_dir: String,

    #[serde(rename = "whisperModel")]
    pub whisper_model: String,
}

impl Config {
    pub fn load(config_path: PathBuf) -> Result<Self, TakeTokError> {
        let file = File::open(config_path)?;
        let reader = BufReader::new(file);
        Ok(serde_json::from_reader(reader)?)
    }
}