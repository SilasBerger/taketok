import {createSignal, Show} from "solid-js";
import {Page} from "../../shared/models";
import LibraryPage from "../../pages/LibraryPage";
import DownloadPage from "../../pages/DownloadPage";
import Navbar from "./Navbar";

function PageCarousel() {

  const [currentPage, setCurrentPage] = createSignal(Page.LIBRARY);

  return (
    <div class="w-full flex flex-col justify-start">
      <Navbar setCurrentPage={setCurrentPage} />
      <Show when={currentPage() == Page.LIBRARY}>
        <LibraryPage />
      </Show>
      <Show when={currentPage() == Page.DOWNLOADS}>
        <DownloadPage />
      </Show>
    </div>
  );
}

export default PageCarousel;