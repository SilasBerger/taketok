use diesel::{ExpressionMethods, RunQueryDsl, SqliteConnection};
use crate::error::TakeTokError;
use crate::schema::author::dsl::author;
use crate::schema;

pub fn insert_author_if_not_exists(conn: &mut SqliteConnection, author_id: &str) -> Result<(), TakeTokError> {
    diesel::insert_or_ignore_into(author)
        .values((schema::author::id.eq(author_id)))
        .execute(conn)?;
    Ok(())
}