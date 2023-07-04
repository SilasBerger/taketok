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
      <video width="400" controls={true} preload="metadata" poster={'http://127.0.0.1:5000/thumbnail/dev/7193720678988746026'}>
        <source src="http://127.0.0.1:5000/video/dev/7193720678988746026" type="video/mp4" />
      </video>


      <table class="table-auto table-border">
        <thead>
        <tr class="table-border">
          <th class="table-border px-2 py-1">ID</th>
          <th class="table-border px-2 py-1">Resolved URL</th>
          <th class="table-border px-2 py-1">Download Date</th>
          <th class="table-border px-2 py-1">Upload Date</th>
          <th class="table-border px-2 py-1">Hashtags</th>
          <th class="table-border px-2 py-1">Author UniqueID</th>
          <th class="table-border px-2 py-1">Author Nickname</th>
          <th class="table-border px-2 py-1">Author Signature</th>
          <th class="table-border px-2 py-1">Transcript</th>
        </tr>
        </thead>
        <tbody>
        <For each={videoData()}>{(video_info: VideoFullInfo) =>
          <tr>
            <td class="table-border px-2 py-1">{video_info.video.id}</td>
            <td class="table-border px-2 py-1">{video_info.video.resolvedUrl}</td>
            <td class="table-border px-2 py-1">{video_info.video.downloadDateIso}</td>
            <td class="table-border px-2 py-1">{video_info.video.uploadDateIso}</td>
            <td class="table-border px-2 py-1">{video_info.hashtags.join(', ')}</td>
            <td class="table-border px-2 py-1">{video_info.video.transcript}</td>
            <td class="table-border px-2 py-1">{video_info.author.uniqueId}</td>
            <td class="table-border px-2 py-1">{video_info.author.nickname}</td>
            <td class="table-border px-2 py-1">{video_info.author.signature}</td>
          </tr>
        }</For>
        </tbody>
      </table>
    </div>
  );
}

export default LibraryPage;