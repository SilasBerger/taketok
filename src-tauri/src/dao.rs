use diesel::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Queryable, Selectable, Serialize, Debug)]
#[diesel(table_name = crate::schema::source_url)]
pub struct SourceUrl {
    pub url: String,
    pub processed: i32,
    pub failure_reason: Option<String>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct TranscriptRequest {
    #[serde(rename = "videoId")]
    pub video_id: String,

    #[serde(rename = "videoOutputDir")]
    pub video_output_dir: String,

    #[serde(rename = "whisperModel")]
    pub whisper_model: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct TranscriptResponse {
    pub transcript: String,
}