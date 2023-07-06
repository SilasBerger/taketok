import {Accessor, createSignal, For, onMount, Show} from "solid-js";
import {VideoFullInfo} from "../shared/models";
import VideoOverlay from "../components/PageCarousel/VideoOverlay";
import VideoCard from "../components/VideoCard/VideoCard";

function LibraryPage({videoData, loadVideoData}: {videoData: Accessor<[VideoFullInfo]>, loadVideoData: () => Promise<void>}) {

  const [playingVideo, setPlayingVideo] = createSignal<VideoFullInfo>();

  onMount(async () => {
    await loadVideoData();
  });

  function playVideo(videoInfo: VideoFullInfo) {
    setPlayingVideo(videoInfo);
  }

  function closeOverlay() {
    if (playingVideo()) {
      setPlayingVideo(undefined);
    }
  }

  return (
    <div>
      <Show when={playingVideo()}>
        <VideoOverlay videoInfo={playingVideo() as VideoFullInfo} onClose={closeOverlay} />
      </Show>

      <div class="grid gap-10
                  grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6
                  px-10 mb-10 mt-20">
        <For each={videoData()}>{(videoInfo: VideoFullInfo) =>
          <VideoCard videoInfo={videoInfo} onClick={() => playVideo(videoInfo)} />
        }</For>
      </div>
    </div>
  );
}

export default LibraryPage;