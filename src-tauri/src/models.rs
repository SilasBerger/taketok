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
    pub video_id: String,
    pub video_output_dir: String,
    pub whisper_model: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct TranscriptResponse {
    pub transcript: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportRequest {
    pub source_url: String,
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
    pub resolved_url: String,
    pub download_date_iso: String,
    pub description: String,
    pub upload_date_iso: String,
    pub hashtags: Vec<String>,
    pub challenges: Vec<ImportResponseChallenge>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ImportResponseAuthor {
    pub id: String,
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
