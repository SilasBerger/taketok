import {Accessor, createSignal, For, onMount, Show} from "solid-js";
import {VideoFullInfo} from "../shared/models";
import VideoOverlay from "../components/PageCarousel/VideoOverlay";
import VideoCard from "../components/VideoCard/VideoCard";

function LibraryPage({videoData, loadVideoData}: {videoData: Accessor<[VideoFullInfo]>, loadVideoData: () => Promise<void>}) {

  const [playingVideo, setPlayingVideo] = createSignal<VideoFullInfo>();
  const [currentSearch, setCurrentSearch] = createSignal('');

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

  const filteredVideos = () => {
    const searchValue = currentSearch().toLowerCase();
    const videos = videoData();

    if (!searchValue) {
      return videos;
    }

    return videos.filter(video => {
      return video.video.description.toLowerCase().includes(searchValue)
        || video.video.transcript?.toLowerCase().includes(searchValue)
    });
  }

  return (
    <div>
      <Show when={playingVideo()}>
        <VideoOverlay videoInfo={playingVideo() as VideoFullInfo} onClose={closeOverlay} />
      </Show>

      <div class="px-10 mt-20">
        <input
          onInput={e => setCurrentSearch(e.target.value)}
          class="w-full rounded-xl border border-solid border-gray-300 text-lg px-4 py-2" />
      </div>
      <div class="grid gap-10
                  grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6
                  px-10 mb-10 mt-10">
        <For each={filteredVideos()}>{(videoInfo: VideoFullInfo) =>
          <VideoCard videoInfo={videoInfo} onClick={() => playVideo(videoInfo)} />
        }</For>
      </div>
    </div>
  );
}

export default LibraryPage;