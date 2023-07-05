import {createSignal, For, onMount, Show} from "solid-js";
import {VideoFullInfo} from "../shared/models";
import VideoOverlay from "../components/PageCarousel/VideoOverlay";

function LibraryPage({videoData, loadVideoData}: {videoData: () => VideoFullInfo[], loadVideoData: () => Promise<void>}) {

  const [playingVideo, setPlayingVideo] = createSignal<string>();

  onMount(async () => {
    await loadVideoData();
  });

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

      <div class="grid gap-10
                  grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6
                  px-10 mb-10 mt-20">
        <For each={videoData()}>{(video_info: VideoFullInfo) =>
          <div class="rounded-2xl relative overflow-hidden cursor-pointer shadow-lg" onclick={() => playVideo(video_info.video.id)}>
            <img width="100%" src={`http://127.0.0.1:5000/thumbnail/dev/${video_info.video.id}`} />
            <div class="absolute bottom-0 z-10
                        h-1/4 hover:h-full
                        bg-gray-100 bg-opacity-60 backdrop-blur-md
                        hover:backdrop-blur-md w-full transition-all">
              This is the description
            </div>
          </div>
        }</For>
      </div>
    </div>
  );
}

export default LibraryPage;