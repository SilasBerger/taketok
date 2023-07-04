use diesel::ConnectionError;
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug, Serialize, Deserialize)]
pub enum TakeTokError {
    #[error("Connection error: {0}")]
    DbConnectionError(String),

    #[error("Database error: {0}")]
    DbError(String),

    #[error("API error: {0}")]
    ApiError(String),

    #[error("IO error: {0}")]
    IoError(String),

    #[error("Serde error: {0}")]
    SerdeError(String),

    #[error("General error: {0}")]
    General(String),
}

impl From<diesel::ConnectionError> for TakeTokError {
    fn from(value: ConnectionError) -> Self {
        TakeTokError::DbConnectionError(value.to_string())
    }
}

impl From<diesel::result::Error> for TakeTokError {
    fn from(value: diesel::result::Error) -> Self {
        TakeTokError::DbError(value.to_string())
    }
}

impl From<reqwest::Error> for TakeTokError {
    fn from(value: reqwest::Error) -> Self {
        TakeTokError::ApiError(value.to_string())
    }
}

impl From<std::io::Error> for TakeTokError {
    fn from(value: std::io::Error) -> Self {
        TakeTokError::IoError(value.to_string())
    }
}

impl From<serde_json::Error> for TakeTokError {
    fn from(value: serde_json::Error) -> Self {
        TakeTokError::SerdeError(value.to_string())
    }
}