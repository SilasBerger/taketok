import {Accessor, createSignal, For, onMount, Show} from "solid-js";
import {VideoFullInfo} from "../shared/models";
import VideoOverlay from "../components/PageCarousel/VideoOverlay";

function LibraryPage({videoData, loadVideoData}: {videoData: Accessor<[VideoFullInfo]>, loadVideoData: () => Promise<void>}) {

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
        <For each={videoData()}>{(videoInfo: VideoFullInfo) =>
          <div class="rounded-2xl relative overflow-hidden cursor-pointer shadow-lg" onclick={() => playVideo(videoInfo.video.id)}>
            <img width="100%" src={`http://127.0.0.1:5000/thumbnail/dev/${videoInfo.video.id}`} />
            <div class="absolute bottom-0 z-10
                        flex flex-col justify-end
                        overflow-hidden
                        h-1/4 hover:h-full
                        bg-gray-100 bg-opacity-60 backdrop-blur-md
                        hover:backdrop-blur-md w-full transition-all">
              <div class="stretch block p-4 overflow-hidden">{videoInfo.video.transcript}</div>
              <div class="text-right py-1 px-4 text-sm">
                by <span class="text-blue-500 font-bold">@{videoInfo.author.nickname}</span>
              </div>
            </div>
          </div>
        }</For>
      </div>
    </div>
  );
}

export default LibraryPage;