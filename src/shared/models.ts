export interface SourceUrl {
  url: string,
  processed: number,
  failure_reason?: string,
}

export interface Video {
  id: string,
  resolvedUrl: string,
  downloadDateIso: string,
  description: string,
  uploadDateIso: string,
  transcript?: string,
}

export interface Author {
  id: string,
  unique_id: string, /* TODO: This is because we receive the DB model and it's not serde-renamed, fix */
  nickname: string,
  signature: string,
  date: string,
}

export interface VideoFullInfo {
  video: Video,
  author: Author,
  hashtags: string[]
}

export enum Page {
  LIBRARY = "Library",
  IMPORT = "Import",
}