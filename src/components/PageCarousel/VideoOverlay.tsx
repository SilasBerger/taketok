import {onMount} from "solid-js";
import {Author, VideoFullInfo} from "../../shared/models";

function VideoOverlay({videoInfo, onClose}: {videoInfo: VideoFullInfo, onClose: () => void}) {

  onMount(async () => {
    await document.querySelector('video')?.play()
  });

  function handleClick(e: MouseEvent) {
    if ((e.target as HTMLElement).id == 'modal') {
      onClose();
    }
  }

  function getAuthorDescription(author: Author): string {
    return author.nickname ? `${author.nickname} (@${author.unique_id})` : `@${author.unique_id}`;
  }

  return (
    <div class="h-screen w-screen fixed p-16 modal backdrop-blur-xl bg-gray-400 bg-opacity-30 z-50" id="modal" onclick={handleClick}>
      <div class="w-full h-full rounded-xl p-10 bg-white relative flex flex-row" id="modal-content">
        <video
          controls={true}
          autoplay={true}
          playsinline
          class="h-full">
          <source src={`http://127.0.0.1:5000/video/dev/${videoInfo.video.id}`} type="video/mp4" />
        </video>
        <div class="ml-6 overflow-scroll">
          <div class="font-bold">
            {videoInfo.video.description} -
            <a class="text-blue-400 underline cursor-pointer" href={videoInfo.video.resolvedUrl}> View on TikTok</a>
          </div>

          <div class="mt-2"></div>
          <div class="italic"><span class="underline">Uploaded</span> {videoInfo.video.upload_date_iso} by <span class="text-blue-400">{getAuthorDescription(videoInfo.author)}</span></div>
          <div class="italic"><span class="underline">Downloaded</span> {videoInfo.video.download_date_iso}</div>

          <div class="mt-6"></div>
          <div>{videoInfo.video.transcript}</div>

        </div>
      </div>
    </div>
  );
}

export default VideoOverlay;