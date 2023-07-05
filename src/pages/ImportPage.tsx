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

  async function importAll() {
    const nonImportedUrls = sourceUrls()
      .filter(sourceUrl => sourceUrl.processed === 0)
      .map(sourceUrl => sourceUrl.url);

    for (let nonImportedUrl of nonImportedUrls) {
      await requestImport(nonImportedUrl);
    }
  }

  async function loadSourceUrls() {
    setSourceUrls(await invoke("fetch_source_urls", {}));
  }

  onMount(async () => {
    await loadSourceUrls();
  })

  return (
    <div class="flex flex-column justify-center mt-20 p-10">
      <table class="w-full table-auto table-border">
        <thead>
        <tr class="table-border">
          <th class="table-border px-2 py-1">URL</th>
          <th class="table-border px-2 py-1">Status</th>
          <th class="table-border px-2 py-1">Interactions</th>
        </tr>
        </thead>
        <tbody>
        <For each={sourceUrls()}>{(sourceUrl: SourceUrl) =>
          <tr>
            <td class="table-border px-2 py-1">{sourceUrl.url}</td>
            <td class="table-border px-2 py-1">{sourceUrl.processed == 0 ? 'Open' : 'Imported'}</td>
            <td class="table-border px-2 py-1">
              <button
                class="btn-primary"
                onClick={async () => await requestImport(sourceUrl.url)}>Import</button>
            </td>
          </tr>
        }</For>
        </tbody>
      </table>
      <div class="absolute top-20 right-10">
        <button
          class="btn-primary"
          onClick={async () => await importAll()}>Import all</button>
      </div>
    </div>
  );
}

export default ImportPage;