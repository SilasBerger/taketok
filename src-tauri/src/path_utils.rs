use std::path::PathBuf;

pub fn taketok_home() -> PathBuf {
    dirs::home_dir().unwrap().join("taketok")
}