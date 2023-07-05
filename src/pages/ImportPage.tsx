import {createSignal, For, onMount} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import {SourceUrl, VideoFullInfo} from "../shared/models";

function ImportPage({loadVideoData}: {loadVideoData: () => Promise<void>}) {

  const [sourceUrls, setSourceUrls] = createSignal<SourceUrl[]>([]);

  async function requestImport(sourceUrl: string) {
    try {
      await invoke("import_from_source_url", {sourceUrl});
      await loadSourceUrls();
      await loadVideoData();
    } catch (e) {
      console.log(e);
    }
  }

  async function loadSourceUrls() {
    setSourceUrls(await invoke("fetch_source_urls", {}));
  }

  onMount(async () => {
    await loadSourceUrls();
  })

  return (
    <div>
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
    </div>
  );
}

export default ImportPage;