import {Portal} from "solid-js/web";
import {onMount} from "solid-js";

function VideoOverlay({videoId, onClose}: {videoId: string, onClose: () => void}) {

  onMount(async () => {
    await document.querySelector('video')?.play()
  });

  function handleClick(e: MouseEvent) {
    if ((e.target as HTMLElement).id == 'modal') {
      onClose();
    }
  }

  return (
    <div class="h-screen w-screen absolute p-16 modal backdrop-blur-sm" id="modal" onclick={handleClick}>
      <div class="w-full h-full rounded-xl p-10 bg-gray-100" id="modal-content">
        <video
          width="200"
          controls={true}
          autoplay={true}
          playsinline>
          <source src={`http://127.0.0.1:5000/video/dev/${videoId}`} type="video/mp4" />
        </video>
      </div>
    </div>
  );
}

export default VideoOverlay;