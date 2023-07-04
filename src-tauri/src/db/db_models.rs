
#![allow(unused)]
#![allow(clippy::all)]

use diesel::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(table_name = crate::db::schema::author)]
pub struct Author {
    pub id: String,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(table_name = crate::db::schema::author_info)]
pub struct AuthorInfo {
    pub id: Option<i32>,
    pub author_id: String,
    pub unique_id: Option<String>,
    pub nickname: Option<String>,
    pub signature: Option<String>,
    pub date: Option<String>,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(table_name = crate::db::schema::challenge)]
pub struct Challenge {
    pub id: String,
    pub title: Option<String>,
    pub description: Option<String>,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(table_name = crate::db::schema::hashtag)]
pub struct Hashtag {
    pub id: i32,
    pub name: String,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize)]
#[diesel(primary_key(url), table_name = crate::db::schema::source_url)]
pub struct SourceUrl {
    pub url: String,
    pub processed: i32,
    pub failure_reason: Option<String>,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(primary_key(schema_version), table_name = crate::db::schema::taketok_schema)]
pub struct TaketokSchema {
    pub schema_version: String,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(table_name = crate::db::schema::video)]
pub struct Video {
    pub id: String,
    pub resolved_url: String,
    pub download_date_iso: Option<String>,
    pub description: Option<String>,
    pub upload_date_iso: Option<String>,
    pub author_id: String,
    pub transcript: Option<String>,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(primary_key(video_id, challenge_id), table_name = crate::db::schema::video_challenge_rel)]
pub struct VideoChallengeRel {
    pub video_id: String,
    pub challenge_id: String,
}

#[derive(Selectable, Queryable, Debug, Identifiable, Insertable, Serialize, Deserialize)]
#[diesel(primary_key(video_id, hashtag_id), table_name = crate::db::schema::video_hashtag_rel)]
pub struct VideoHashtagRel {
    pub video_id: String,
    pub hashtag_id: i32,
}
