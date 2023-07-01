use diesel::prelude::*;

#[derive(Queryable, Selectable, Debug)]
#[diesel(table_name = crate::schema::source_urls)]
pub struct SourceUrls {
    pub url: String,
    pub processed: i32,
    pub failure_reason: Option<String>,
}

#[derive(Queryable, Selectable, Debug)]
#[diesel(table_name = crate::schema::author)]
pub struct Author {
    pub id: String,
}