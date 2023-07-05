import {createSignal, For, onMount, Show} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import {VideoFullInfo} from "../shared/models";
import VideoOverlay from "../components/PageCarousel/VideoOverlay";

function LibraryPage() {

  const [videoData, setVideoData] = createSignal<VideoFullInfo[]>([])
  const [playingVideo, setPlayingVideo] = createSignal<string>();

  onMount(async () => {
    setVideoData(await invoke("get_all_video_data", {}));
  })

  function playVideo(videoId: string) {
    setPlayingVideo(videoId);
  }

  function closeOverlay() {
    if (playingVideo()) {
      setPlayingVideo(undefined);
    }
  }

  return (
    <div>
      <Show when={playingVideo()}>
        <VideoOverlay videoId={playingVideo() as string} onClose={closeOverlay} />
      </Show>

      <div class="grid grid-cols-4 grid-rows-max bg-amber-50">
        <For each={videoData()}>{(video_info: VideoFullInfo) =>
          <div class="rounded-2xl overflow-hidden cursor-pointer p-1 bg-purple-200" onclick={() => playVideo(video_info.video.id)}>
            <img width="100%" src={`http://127.0.0.1:5000/thumbnail/dev/${video_info.video.id}`} />
          </div>
        }</For>
      </div>
    </div>
  );
}

export default LibraryPage;