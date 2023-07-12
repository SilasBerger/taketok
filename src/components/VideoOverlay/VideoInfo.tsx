import {Author, VideoFullInfo} from "../../shared/models";

function getAuthorDescription(author: Author): string {
  return author.nickname ? `${author.nickname} (@${author.unique_id})` : `@${author.unique_id}`;
}

function VideoInfo({videoInfo}: {videoInfo: VideoFullInfo}) {
  return (
    <div class="ml-6 overflow-scroll">
      <div class="font-bold">
        {videoInfo.video.description} -
        <a class="text-blue-400 underline cursor-pointer" href={videoInfo.video.resolvedUrl}> View on TikTok</a>
      </div>

      <div class="mt-2"></div>
      <div class="italic">
        <span class="underline">Uploaded</span> {videoInfo.video.upload_date_iso}
        <span> by </span><span class="text-blue-400">{getAuthorDescription(videoInfo.author)}</span>
      </div>
      <div class="italic"><span class="underline">Downloaded</span> {videoInfo.video.download_date_iso}</div>

      <div class="mt-6"></div>

      <div>{videoInfo.video.transcript}</div>
    </div>
  );
}

export default VideoInfo;