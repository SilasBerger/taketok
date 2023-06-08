drop table if exists video_challenge_rel;
drop table if exists challenge;
drop table if exists video_hashtag_rel;
drop table if exists hashtag;
drop table if exists video;
drop table if exists author_data;
drop table if exists author;
drop table if exists taketok_schema;

create table taketok_schema (
    schema_version unique not null
);

create table author (
    author_id text unique not null
);

create table author_data (
    author_rowid references author(ROWID) on delete cascade,
    id text,
    unique_id text,
    nickname text,
    signature text,
    date text
);

create table video (
    source_url text unique not null,
    resolved_url text unique,
    download_status text,
    video_id text unique,
    download_date_iso text,
    description text,
    upload_date_iso text,
    author_rowid references author(ROWID),
    transcript text
);

create table hashtag (
    hashtag text not null
);

create table video_hashtag_rel (
    video_rowid references video(ROWID) on delete cascade,
    hashtag_rowid references hashtag(ROWID) on delete cascade,
    primary key (video_rowid, hashtag_rowid)
);

create table challenge (
    id text not null,
    title,
    description
);

create table video_challenge_rel (
    video_rowid references video(ROWID) on delete cascade,
    challenge_rowid references challenge(ROWID) on delete cascade,
    primary key (video_rowid, challenge_rowid)
);

insert into taketok_schema (schema_version) values ('1.0');