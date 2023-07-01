// @generated automatically by Diesel CLI.

diesel::table! {
    author (id) {
        id -> Text,
    }
}

diesel::table! {
    author_info (id) {
        id -> Nullable<Integer>,
        author_id -> Text,
        unique_id -> Nullable<Text>,
        nickname -> Nullable<Text>,
        signature -> Nullable<Text>,
        date -> Nullable<Text>,
    }
}

diesel::table! {
    challenge (id) {
        id -> Text,
        title -> Nullable<Text>,
        description -> Nullable<Text>,
    }
}

diesel::table! {
    hashtag (id) {
        id -> Nullable<Integer>,
        name -> Text,
    }
}

diesel::table! {
    source_urls (url) {
        url -> Text,
        processed -> Integer,
        failure_reason -> Nullable<Text>,
    }
}

diesel::table! {
    taketok_schema (schema_version) {
        schema_version -> Text,
    }
}

diesel::table! {
    video (id) {
        id -> Text,
        resolved_url -> Nullable<Text>,
        download_date_iso -> Nullable<Text>,
        description -> Nullable<Text>,
        upload_date_iso -> Nullable<Text>,
        author_id -> Nullable<Text>,
        transcript -> Nullable<Text>,
    }
}

diesel::table! {
    video_challenge_rel (video_id, challenge_id) {
        video_id -> Text,
        challenge_id -> Text,
    }
}

diesel::table! {
    video_hashtag_rel (video_id, hashtag_id) {
        video_id -> Text,
        hashtag_id -> Integer,
    }
}

diesel::joinable!(author_info -> author (author_id));
diesel::joinable!(video -> author (author_id));
diesel::joinable!(video_challenge_rel -> challenge (challenge_id));
diesel::joinable!(video_challenge_rel -> video (video_id));
diesel::joinable!(video_hashtag_rel -> hashtag (hashtag_id));
diesel::joinable!(video_hashtag_rel -> video (video_id));

diesel::allow_tables_to_appear_in_same_query!(
    author,
    author_info,
    challenge,
    hashtag,
    source_urls,
    taketok_schema,
    video,
    video_challenge_rel,
    video_hashtag_rel,
);
