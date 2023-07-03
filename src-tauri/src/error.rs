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
