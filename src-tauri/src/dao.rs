use diesel::prelude::*;

#[derive(Queryable, Selectable, Debug)]
#[diesel(table_name = crate::schema::source_urls)]
pub struct SourceUrls {
    pub url: String,
    pub processed: bool,
    pub failure_reason: Option<String>,
}