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

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportRequest {
    #[serde(rename = "sourceUrl")]
    pub source_url: String,

    #[serde(rename = "videoOutputDir")]
    pub video_output_dir: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportResponse {
    pub video: ImportResponseVideo,
    pub author: ImportResponseAuthor,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportResponseVideo {
    pub id: String,

    #[serde(rename = "resolvedUrl")]
    pub resolved_url: String,

    #[serde(rename = "downloadDateIso")]
    pub download_date_iso: String,

    pub description: String,

    #[serde(rename = "uploadDateIso")]
    pub upload_date_iso: String,

    pub hashtags: Vec<String>,

    pub challenges: Vec<ImportResponseChallenge>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportResponseAuthor {
    pub id: String,

    #[serde(rename = "uniqueId")]
    pub unique_id: String,

    pub nickname: String,

    pub signature: String,

    pub date: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportResponseChallenge {
    pub id: String,
    pub title: String,
    pub description: String,
}
