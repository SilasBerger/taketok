use std::env::current_dir;
use std::path::PathBuf;

pub fn taketok_home() -> PathBuf {
    dirs::home_dir().unwrap().join("taketok")
}

pub fn config_file(config_name: &str) -> PathBuf {
    taketok_home().join("config").join(&format!("{}.config.json", config_name))
}

pub fn resources_dir() -> PathBuf {
    current_dir().unwrap().join("resources")
}

pub fn mock_api_data_file(data_file_name: &str) -> PathBuf {
    resources_dir().join("mock_api_data").join(&format!("{}.json", data_file_name))
}