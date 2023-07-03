use std::path::PathBuf;

pub fn taketok_home() -> PathBuf {
    dirs::home_dir().unwrap().join("taketok")
}

pub fn config_file(config_name: &str) -> PathBuf {
    taketok_home().join("config").join(&format!("{}.config.json", config_name))
}