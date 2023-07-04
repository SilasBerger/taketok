use std::ops::Mul;
use std::path::PathBuf;
use std::time::Duration;
use serde::{Deserialize, Serialize};
use crate::core_api_client::OpMode::{Live, Mock};
use crate::error::TakeTokError;
use crate::models::{ImportRequest, ImportResponse, ImportResponseVideo, TranscriptRequest, TranscriptResponse};
use crate::path_utils::mock_api_data_file;
use crate::utils::read_as_json;

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

    pub fn mock(data_file_name: &str) -> Self {
        let data_file_path = mock_api_data_file(data_file_name);
        let mock_data = read_as_json(&data_file_path)
            .expect(&format!("Unable to read mock data from path: {:?}", &data_file_path));

        Self {
            op_mode: Mock(CoreApiClientMock { mock_data })
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
    mock_data: CoreApiMockData
}

impl CoreApiClientMock {
    fn get_fake_video_metadata(&self, source_url: &str) -> Result<ImportResponse, TakeTokError> {
        let matching_entry = &self.mock_data.video_metadata
            .iter()
            .find(|&entry| entry.source_url.eq(source_url));

        match matching_entry {
            Some(entry) => {
                match &entry.entry {
                    Some(response) => Ok(response.clone()),
                    None => Err(TakeTokError::General("This is a fake error for that entry".to_string()))
                }
            }
            None => Err(TakeTokError::General("No entry found".to_string()))
        }
    }

    fn get_fake_transcript(&self, video_id: &str) -> Result<String, TakeTokError> {
        let matching_entry = &self.mock_data.transcripts
            .iter()
            .find(|&entry| entry.video_id.eq(video_id));

        match matching_entry {
            Some(entry) => {
                Ok(entry.entry.transcript.to_string())
            }
            None => Err(TakeTokError::General("No transcript found".to_string()))
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct CoreApiMockImportResponseEntry {
    #[serde(rename = "sourceUrl")]
    pub source_url: String,
    pub entry: Option<ImportResponse>,
}

#[derive(Serialize, Deserialize, Debug)]
struct CoreApiMockTranscriptEntry {
    #[serde(rename = "videoId")]
    pub video_id: String,
    pub entry: TranscriptResponse,
}

#[derive(Serialize, Deserialize, Debug)]
struct CoreApiMockData {
    #[serde(rename = "videoMetadata")]
    pub video_metadata: Vec<CoreApiMockImportResponseEntry>,
    pub transcripts: Vec<CoreApiMockTranscriptEntry>
}