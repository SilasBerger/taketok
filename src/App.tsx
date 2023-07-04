import {createSignal, For, onMount, Show} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";

function App() {

  const [sourceUrls, setSourceUrls] = createSignal<SourceUrl[]>([]);
  const [videoData, setVideoData] = createSignal<VideoFullInfo[]>([])

  interface SourceUrl {
    url: string,
    processed: number,
    failure_reason?: string,
  }

  interface Video {
      id: string,
      resolvedUrl: string,
      downloadDateIso: string,
      description: string,
      uploadDateIso: string,
      transcript?: string,
  }

  interface Author {
    id: string,
    uniqueId: string,
    nickname: string,
    signature: string,
    date: string,
  }

  interface VideoFullInfo {
    video: Video,
    author: Author,
    hashtags: string[]
  }

  async function requestImport(sourceUrl: string) {
    try {
      await invoke("import_from_source_url", {sourceUrl});
      setVideoData(await invoke("get_all_video_data", {}));
    } catch (e) {
      console.log(e);
    }
  }

  function registerToggleDevtoolsKeyboardTrigger() {
    // TODO: Not very nice, refactor at some point...
    window.onkeyup = async (event) => {
      if (event.key == 'F12') {
        try {
          await invoke("toggle_devtools", {});
        } catch (e) {
          console.log(e);
        }
      }
    }
  }

  onMount(async () => {
    setSourceUrls(await invoke("fetch_source_urls", {}));
    setVideoData(await invoke("get_all_video_data", {}));
    registerToggleDevtoolsKeyboardTrigger();
  })

  return (
    <div class="flex flex-col items-center justify-start max-w-full m-7">

      <video width="400" controls={true} preload="metadata" poster={'http://127.0.0.1:5000/thumbnail/dev/7193720678988746026'}>
        <source src="http://127.0.0.1:5000/video/dev/7193720678988746026" type="video/mp4" />
      </video>

      <table class="table-auto table-border">
        <thead>
          <tr class="table-border">
            <th class="table-border px-2 py-1">URL</th>
            <th class="table-border px-2 py-1">Processed?</th>
            <th class="table-border px-2 py-1">Interactions</th>
          </tr>
        </thead>
        <tbody>
          <For each={sourceUrls()}>{(sourceUrl: SourceUrl) =>
            <tr>
              <td class="table-border px-2 py-1">{sourceUrl.url}</td>
              <td class="table-border px-2 py-1">{sourceUrl.processed}</td>
              <td class="table-border px-2 py-1">
                <button
                  class="rounded-3xl px-4 py-2 bg-purple-200 hover:bg-purple-300 transition-all duration-150"
                  onClick={() => requestImport(sourceUrl.url)}>Import</button>
              </td>
            </tr>
          }</For>
        </tbody>
      </table>

      <div class="mt-4"></div>

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

export default App;
