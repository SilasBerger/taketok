use diesel::prelude::*;

#[derive(Queryable, Selectable, Debug)]
#[diesel(table_name = crate::schema::source_url)]
pub struct SourceUrl {
    pub url: String,
    pub processed: i32,
    pub failure_reason: Option<String>,
}
