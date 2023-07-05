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
    <div class="flex flex-col justify-center mt-12 p-10">
      <div class="flex flex-row justify-end items-center mb-10">
        <div class={`grow font-bold text-2xl`}>
          Source URLs
        </div>
        <button
          class="btn-primary"
          onClick={async () => await importAll()}>Import all</button>
      </div>

      <For each={sourceUrls().filter(sourceUrl => sourceUrl.processed === 0)}>{(sourceUrl: SourceUrl) =>
        <div class={`flex flex-row justify-end mb-2 bg-gray-100 rounded-xl overflow-hidden`}>
          <div class={`grow p-5 underline`}>{sourceUrl.url}</div>
          <div class={`flex justify-center items-center bg-green-200 hover:bg-green-300 transition:all`}>
            <button
              class={`block w-full h-full px-10`}
              onclick={() => requestImport(sourceUrl.url)}>Import</button>
          </div>
        </div>
      }</For>
    </div>
  );
}

export default ImportPage;