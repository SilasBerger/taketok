use serde::{Deserialize, Serialize};
use crate::db::db_models::{AuthorInfo, Video};

#[derive(Serialize, Deserialize, Debug)]
pub struct TranscriptRequest {
    #[serde(rename = "videoId")]
    pub video_id: String,

    #[serde(rename = "configName")]
    pub config_name: String,

    #[serde(rename = "whisperModel")]
    pub whisper_model: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct TranscriptResponse {
    pub transcript: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportRequest {
    #[serde(rename = "sourceUrl")]
    pub source_url: String,

    #[serde(rename = "configName")]
    pub config_name: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ImportResponse {
    pub video: ImportResponseVideo,
    pub author: ImportResponseAuthor,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
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

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ImportResponseAuthor {
    pub id: String,

    #[serde(rename = "uniqueId")]
    pub unique_id: Option<String>,

    pub nickname: Option<String>,

    pub signature: Option<String>,

    pub date: Option<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ImportResponseChallenge {
    pub id: String,
    pub title: String,
    pub description: String,
}

#[derive(Serialize, Deserialize)]
pub struct VideoFullInfo {
    pub video: Video,
    pub author: AuthorInfo,
    pub hashtags: Vec<String>,
}