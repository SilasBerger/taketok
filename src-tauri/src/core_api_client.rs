use std::ops::Mul;
use std::time::Duration;
use crate::core_api_client::OpMode::{Live, Mock};
use crate::error::TakeTokError;
use crate::models::{TranscriptRequest, TranscriptResponse};

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

    pub async fn request_transcript(&self) -> Result<String, TakeTokError> {
        match &self.op_mode {
            Live(client) => client.request_transcript().await,
            Mock(client) => client.get_fake_transcript()
        }
    }
}

struct CoreApiClientImpl {

}

impl CoreApiClientImpl {
    pub async fn request_transcript(&self) -> Result<String, TakeTokError> {
        let client = reqwest::Client::new();

        let request_body = TranscriptRequest {
            video_id: "7202782477717343531".to_string(),
            video_output_dir: "/Users/silas/taketok/videos/dev".to_string(),
            whisper_model: "small".to_string(),
        };

        let result = client
            .post("http://127.0.0.1:5000/transcribe")
            .timeout(Duration::from_secs(60).mul(10))
            .json(&request_body)
            .send()
            .await?;

        let transcript_response: TranscriptResponse = result.json().await?;
        Ok(transcript_response.transcript.to_string())
    }
}

struct CoreApiClientMock {

}

impl CoreApiClientMock {
    fn get_fake_transcript(&self) -> Result<String, TakeTokError> {
        Ok("This is not the greatest code in the world, this is just a transcript.".to_string())
    }
}
