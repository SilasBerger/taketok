import {createSignal, For} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";

function App() {

  const [sourceUrls, setSourceUrls] = createSignal<SourceUrl[]>([]);
  const [transcript, setTranscript] = createSignal("");

  interface SourceUrl {
    url: string,
    processed: number,
    failure_reason?: string,
  }

  async function fetchSourceUrls() {
    console.log("trying to fetch source urls");
    setSourceUrls(await invoke("fetch_source_urls", {}));
  }

  async function requestATranscript() {
    const transcript: string = await invoke("request_a_transcript", {});
    setTranscript(transcript);
  }

  return (
    <div class="flex flex-col items-center max-w-full mt-7">
      <button
        class="rounded-3xl p-2 ps-4 pe-4 bg-purple-200"
        onClick={fetchSourceUrls}>Fetch source URLs</button>
      <button
        class="rounded-3xl p-2 ps-4 pe-4 bg-purple-200"
        onClick={requestATranscript}>Request a transcript</button>

      <h2>Source URLs</h2>
      <table class="table-auto">
        <thead>
          <tr>
            <th>URL</th>
            <th>Processed?</th>
            <th>Failure Reason</th>
          </tr>
        </thead>
        <tbody>
          <For each={sourceUrls()}>{(sourceUrl: SourceUrl) =>
            <tr>
              <td>{sourceUrl.url}</td>
              <td>{sourceUrl.processed}</td>
              <td>{sourceUrl.failure_reason}</td>
            </tr>
          }</For>
        </tbody>
      </table>

      <h2>Transcript</h2>
      <span>{transcript()}</span>
    </div>
  );
}

export default App;
