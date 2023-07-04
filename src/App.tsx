import {createSignal, For, onMount, Show} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";
import DownloadPage from "./pages/DownloadPage";
import LibraryPage from "./pages/LibraryPage";

function App() {


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
    registerToggleDevtoolsKeyboardTrigger();
  })

  return (
    <div class="flex flex-col items-center justify-start max-w-full m-7">
      <DownloadPage />
      <div class="mt-4"></div>
      <LibraryPage />
    </div>
  );
}

export default App;
