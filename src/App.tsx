import {createSignal, For, onMount, Show} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";

function App() {

  const [sourceUrls, setSourceUrls] = createSignal<SourceUrl[]>([]);
  const [
    videosDict,
    setVideosDict
  ] = createSignal<{[key: string]: ImportResponse}>({});

  const videos = () => Object.values(videosDict());

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
      hashtags: string[],
      challenges: Challenge[],
      transcript?: string,
  }

  interface Challenge {
     id: string,
     title: string,
     description: string,
  }

  interface Author {
    id: string,
    uniqueId: string,
    nickname: string,
    signature: string,
    date: string,
  }

  interface ImportResponse {
    video: Video,
    author: Author,
  }

  async function requestTranscript(videoId: string) {
    try {
      const transcript: string = await invoke("request_transcript", {videoId});
      const nextVideosDict = {...videosDict()};
      const oldVideo = nextVideosDict[videoId];
      nextVideosDict[videoId] = {
        ...oldVideo,
        video: {...oldVideo.video, transcript: transcript},
      };
      setVideosDict(nextVideosDict);
    } catch (e) {
      console.log(e);
    }
  }

  async function requestImport(sourceUrl: string) {
    try {
      const result: ImportResponse = await invoke("import_from_source_url", {sourceUrl});
      console.log('Success!');
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
    registerToggleDevtoolsKeyboardTrigger();
  })

  return (
    <div class="flex flex-col items-center justify-start max-w-full m-7">
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
        <For each={videos()}>{(video: ImportResponse) =>
          <tr>
            <td class="table-border px-2 py-1">{video.video.id}</td>
            <td class="table-border px-2 py-1">{video.video.resolvedUrl}</td>
            <td class="table-border px-2 py-1">{video.video.downloadDateIso}</td>
            <td class="table-border px-2 py-1">{video.video.uploadDateIso}</td>
            <td class="table-border px-2 py-1">{video.video.hashtags.join(', ')}</td>
            <td class="table-border px-2 py-1">{video.author.uniqueId}</td>
            <td class="table-border px-2 py-1">{video.author.nickname}</td>
            <td class="table-border px-2 py-1">{video.author.signature}</td>
            <td class="table-border px-2 py-1">
              <Show
                when={video.video.transcript}
                fallback={
                  <button class="rounded-3xl px-4 py-2 bg-purple-200 hover:bg-purple-300 transition-all duration-150"
                        onClick={() => requestTranscript(video.video.id)}>Transcribe</button>}>
                <div>{video.video.transcript}</div>
              </Show>
            </td>
          </tr>
        }</For>
        </tbody>
      </table>
    </div>
  );
}

export default App;
