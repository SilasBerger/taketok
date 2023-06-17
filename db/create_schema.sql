drop table if exists video_challenge_rel;
drop table if exists challenge;
drop table if exists video_hashtag_rel;
drop table if exists hashtag;
drop table if exists video;
drop table if exists author_info;
drop table if exists author;
drop table if exists source_urls;
drop table if exists taketok_schema;

create table taketok_schema (
    schema_version primary key
) without rowid;

create table source_urls(
    url text primary key not null,
    processed integer not null default false,
    failure_reason text
) without rowid;

create table author (
    id text primary key not null
) without rowid;

create table author_info (
    id integer primary key autoincrement,
    author_id text not null references author(id) on delete cascade,
    unique_id text,
    nickname text,
    signature text,
    date text
);

create table video (
    id text primary key not null,
    resolved_url text unique,
    download_date_iso text,
    description text,
    upload_date_iso text,
    author_id references author(id),
    transcript text
) without rowid;

create table hashtag (
    id integer primary key autoincrement,
    name text unique not null
);

create table video_hashtag_rel (
    video_id not null references video(id) on delete cascade,
    hashtag_id not null references hashtag(id) on delete cascade,
    primary key (video_id, hashtag_id)
) without rowid;

create table challenge (
    id text primary key not null,
    title,
    description
) without rowid;

create table video_challenge_rel (
    video_id not null references video(id) on delete cascade,
    challenge_id not null references challenge(id) on delete cascade,
    primary key (video_id, challenge_id)
) without rowid;

insert into taketok_schema (schema_version) values ('1.0');