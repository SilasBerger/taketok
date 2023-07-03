use std::ops::Mul;
use std::time::Duration;
use crate::core_api_client::OpMode::{Live, Mock};
use crate::error::TakeTokError;
use crate::models::{ImportRequest, ImportResponse, ImportResponseVideo, TranscriptRequest, TranscriptResponse};

pub struct CoreApiClient {
    op_mode: OpMode,
}

enum OpMode {
    Live(CoreApiClientImpl),
    Mock(CoreApiClientMock),
}

impl CoreApiClient {
    pub fn new() -> Self {
        Self {
            op_mode: Live(CoreApiClientImpl {})
        }
    }

    pub fn mock() -> Self {
        Self {
            op_mode: Mock(CoreApiClientMock {})
        }
    }

    pub async fn import_from_source_url(&self, source_url: &str, video_output_dir: &str) -> Result<ImportResponse, TakeTokError> {
        match &self.op_mode {
            Live(client) => client.import_from_source_url(source_url, video_output_dir).await,
            Mock(client) => client.get_fake_video_metadata(source_url),
        }
    }

    pub async fn request_transcript(&self, video_id: &str, video_output_dir: &str, whisper_model: &str) -> Result<String, TakeTokError> {
        match &self.op_mode {
            Live(client) => client.request_transcript(video_id, video_output_dir, whisper_model).await,
            Mock(client) => client.get_fake_transcript(video_id),
        }
    }
}

struct CoreApiClientImpl {

}

impl CoreApiClientImpl {
    pub async fn import_from_source_url(&self, source_url: &str, video_output_dir: &str) -> Result<ImportResponse, TakeTokError> {
        let client = reqwest::Client::new();

        let request_body = ImportRequest {
            source_url: source_url.to_string(),
            video_output_dir: video_output_dir.to_string(),
        };

        println!("{:?}", request_body);

        let result = client
            .post("http://127.0.0.1:5000/import-from-source-url")
            .timeout(Duration::from_secs(60).mul(10))
            .json(&request_body)
            .send()
            .await?;

        Ok(result.json().await?)
    }

    pub async fn request_transcript(&self, video_id: &str, video_output_dir: &str, whisper_model: &str) -> Result<String, TakeTokError> {
        let client = reqwest::Client::new();

        let request_body = TranscriptRequest {
            video_id: video_id.to_string(),
            video_output_dir: video_output_dir.to_string(),
            whisper_model: whisper_model.to_string(),
        };

        let result = client
            .post("http://127.0.0.1:5000/transcribe")
            .timeout(Duration::from_secs(60).mul(10))
            .json(&request_body)
            .send()
            .await?;

        let transcript_response: TranscriptResponse = result.json().await?;
        Ok(transcript_response.transcript)
    }
}

struct CoreApiClientMock {

}

impl CoreApiClientMock {
    fn get_fake_transcript(&self, video_id: &str) -> Result<String, TakeTokError> {
        Ok(format!("This is not the greatest code in the world, this is just a transcript for video {}.", video_id))
    }

    fn get_fake_video_metadata(&self, source_url: &str) -> Result<ImportResponse, TakeTokError> {
        Err(TakeTokError::General(format!("Not yet implemented")))
    }
}
