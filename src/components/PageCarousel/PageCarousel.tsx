import {createSignal, Show} from "solid-js";
import {Page, VideoFullInfo} from "../../shared/models";
import LibraryPage from "../../pages/LibraryPage";
import ImportPage from "../../pages/ImportPage";
import Navbar from "./Navbar";
import {invoke} from "@tauri-apps/api/tauri";

function PageCarousel() {

  const [currentPage, setCurrentPage] = createSignal(Page.LIBRARY);
  const [videoData, setVideoData] = createSignal<VideoFullInfo[]>([])

  async function loadVideoData() {
    setVideoData(await invoke("get_all_video_data", {}));
  }

  return (
    <div class="w-full flex flex-col justify-start">
      <Navbar setCurrentPage={setCurrentPage} />
      <Show when={currentPage() == Page.LIBRARY}>
        <LibraryPage videoData={videoData} loadVideoData={loadVideoData} />
      </Show>
      <Show when={currentPage() == Page.IMPORT}>
        <ImportPage loadVideoData={loadVideoData} />
      </Show>
    </div>
  );
}

export default PageCarousel;