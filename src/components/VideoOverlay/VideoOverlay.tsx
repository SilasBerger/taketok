import {onMount} from "solid-js";
import {Author, VideoFullInfo} from "../../shared/models";
import TikTokVideo from "./TikTokVideo";
import VideoInfo from "./VideoInfo";

function VideoOverlay({videoInfo, onClose}: {videoInfo: VideoFullInfo, onClose: () => void}) {

  onMount(async () => {
    await document.querySelector('video')?.play()
  });

  function closeModalOnOutsideClick(e: MouseEvent) {
    if ((e.target as HTMLElement).id == 'modal') {
      onClose();
    }
  }

  return (
    <div class="modal fixed z-50 h-screen w-screen p-16 backdrop-blur-xl bg-gray-400 bg-opacity-30"
         id="modal"
         onclick={closeModalOnOutsideClick}>
      <div class="w-full h-full rounded-xl p-10 bg-white relative flex flex-row" id="modal-content">
        <TikTokVideo videoId={videoInfo.video.id} />
        <VideoInfo videoInfo={videoInfo} />
      </div>
    </div>
  );
}

export default VideoOverlay;