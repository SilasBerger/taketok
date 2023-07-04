import {createSignal, For, onMount} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import {VideoFullInfo} from "../shared/models";

function LibraryPage() {

  const [videoData, setVideoData] = createSignal<VideoFullInfo[]>([])

  onMount(async () => {
    setVideoData(await invoke("get_all_video_data", {}));
  })

  return (
    <div>
      <For each={videoData()}>{(video_info: VideoFullInfo) =>
        <video
          width="200"
          controls={true}
          preload="metadata"
          poster={`http://127.0.0.1:5000/thumbnail/dev/${video_info.video.id}`}>
          <source src={`http://127.0.0.1:5000/video/dev/${video_info.video.id}`} type="video/mp4" />
        </video>
      }</For>
    </div>
  );
}

export default LibraryPage;