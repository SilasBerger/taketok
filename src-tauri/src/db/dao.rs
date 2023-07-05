use diesel::{ExpressionMethods, insert_into, insert_or_ignore_into, OptionalExtension, QueryDsl, RunQueryDsl, SelectableHelper, SqliteConnection, update};
use crate::db::db_models::{AuthorInfo, Hashtag, Video};
use crate::db::schema;
use crate::db::schema::source_url::dsl::source_url;
use crate::error::TakeTokError;
use crate::models::{ImportResponseAuthor, ImportResponseChallenge, ImportResponseVideo, VideoFullInfo};

pub fn insert_author_if_not_exists(conn: &mut SqliteConnection, author_id: &str) -> Result<(), TakeTokError> {
    use crate::db::schema::author::dsl::author;
    use crate::db::schema::author::id;

    insert_or_ignore_into(author)
        .values((id.eq(author_id)))
        .execute(conn)?;
    Ok(())
}

pub fn update_author_info_if_changed(conn: &mut SqliteConnection, author_data: &ImportResponseAuthor) -> Result<(), TakeTokError> {
    use crate::db::schema::author_info;

    let latest_author_info = author_info::dsl::author_info
        .select(AuthorInfo::as_select())
        .filter(author_info::author_id.eq(&author_data.id))
        .order_by(author_info::date.desc())
        .first(conn)
        .optional()?;

    let do_insert = if let Some(result) = latest_author_info {
        let latest_stored = (&result.unique_id, &result.nickname, &result.signature);
        let new_data = (&author_data.unique_id, &author_data.nickname, &author_data.signature);
        !latest_stored.eq(&new_data)
    } else {
        true
    };

    if !do_insert {
        return Ok(())
    }

    insert_into(author_info::dsl::author_info)
        .values((
            author_info::author_id.eq(&author_data.id),
            author_info::unique_id.eq(&author_data.unique_id),
            author_info::nickname.eq(&author_data.nickname),
            author_info::signature.eq(&author_data.signature),
            author_info::date.eq(&author_data.date),
        ))
        .execute(conn)?;

    Ok(())
}

pub fn save_video_metadata(conn: &mut SqliteConnection, video_data: &ImportResponseVideo, author_id: &str) -> Result<(), TakeTokError> {
    use crate::db::schema::video;

    insert_into(video::dsl::video)
        .values((
            video::id.eq(&video_data.id),
            video::resolved_url.eq(&video_data.resolved_url),
            video::download_date_iso.eq(&video_data.download_date_iso),
            video::description.eq(&video_data.description),
            video::upload_date_iso.eq(&video_data.upload_date_iso),
            video::author_id.eq(author_id),
        ))
        .execute(conn)?;

    Ok(())
}

pub fn insert_hashtags(conn: &mut SqliteConnection, video_id: &str, hashtags: &Vec<String>) -> Result<(), TakeTokError> {
    use crate::db::schema::hashtag;
    use crate::db::schema::video_hashtag_rel;

    for hashtag_to_insert in hashtags {
        insert_or_ignore_into(hashtag::dsl::hashtag)
            .values(hashtag::name.eq(hashtag_to_insert))
            .execute(conn)?;

        let hashtag_id = hashtag::dsl::hashtag
            .select(Hashtag::as_select())
            .filter(hashtag::name.eq(hashtag_to_insert))
            .first(conn)?
            .id;

        insert_or_ignore_into(video_hashtag_rel::dsl::video_hashtag_rel)
            .values((
                video_hashtag_rel::video_id.eq(video_id),
                video_hashtag_rel::hashtag_id.eq(hashtag_id),
            ))
            .execute(conn)?;
    }

    Ok(())
}

pub fn insert_challenges(conn: &mut SqliteConnection, video_id: &str, challenges: &Vec<ImportResponseChallenge>) -> Result<(), TakeTokError> {
    use crate::db::schema::challenge;
    use crate::db::schema::video_challenge_rel;

    for challenge_to_insert in challenges {
        insert_or_ignore_into(challenge::dsl::challenge)
            .values((
                challenge::id.eq(&challenge_to_insert.id),
                challenge::title.eq(&challenge_to_insert.title),
                challenge::description.eq(&challenge_to_insert.description),
            ))
            .execute(conn)?;

        insert_or_ignore_into(video_challenge_rel::dsl::video_challenge_rel)
            .values((
                video_challenge_rel::video_id.eq(video_id),
                video_challenge_rel::challenge_id.eq(&challenge_to_insert.id),
            ))
            .execute(conn)?;
    }

    Ok(())
}

pub fn insert_transcript(conn: &mut SqliteConnection, video_id: &str, transcript: &str) -> Result<(), TakeTokError> {
    use crate::db::schema::video;

    diesel::update(video::dsl::video)
        .filter(video::id.eq(video_id))
        .set(video::transcript.eq(transcript))
        .execute(conn)?;

    Ok(())
}

pub fn load_all_video_data(conn: &mut SqliteConnection) -> Result<Vec<VideoFullInfo>, TakeTokError> {
    use crate::db::schema::video;
    use crate::db::schema::author_info;
    use crate::db::schema::video_hashtag_rel;
    use crate::db::schema::hashtag;

    let mut result = vec![];

    let videos = video::dsl::video
        .select(Video::as_select())
        .load(conn)?;

    for loaded_video in videos {
        let author = author_info::dsl::author_info
            .select(AuthorInfo::as_select())
            .filter(author_info::author_id.eq(&loaded_video.author_id))
            .order_by(author_info::date.desc())
            .first(conn)?;

        let hashtags: Vec<String> = video_hashtag_rel::dsl::video_hashtag_rel
            .inner_join(hashtag::dsl::hashtag)
            .select(hashtag::name)
            .filter(video_hashtag_rel::video_id.eq(&loaded_video.id))
            .load(conn)?;

        result.push(VideoFullInfo {
            video: loaded_video,
            author,
            hashtags,
        });
    }

    Ok(result)
}

pub fn mark_source_as_processed(conn: &mut SqliteConnection, processed_source_url: &str) -> Result<(), TakeTokError> {
    use crate::db::schema::source_url;
    
    update(source_url)
        .filter(source_url::url.eq(processed_source_url))
        .set(source_url::processed.eq(1))
        .execute(conn)?;
        
    Ok(())
}