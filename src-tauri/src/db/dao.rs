use diesel::{ExpressionMethods, OptionalExtension, QueryDsl, QueryResult, RunQueryDsl, SelectableHelper, SqliteConnection};
use diesel::internal::derives::multiconnection::SelectStatementAccessor;
use crate::db::db_models::AuthorInfo;
use crate::error::TakeTokError;
use crate::models::{ImportResponseAuthor};

pub fn insert_author_if_not_exists(conn: &mut SqliteConnection, author_id: &str) -> Result<(), TakeTokError> {
    use crate::db::schema::author::dsl::author;
    use crate::db::schema::author::id;

    diesel::insert_or_ignore_into(author)
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

    diesel::insert_into(author_info::dsl::author_info)
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