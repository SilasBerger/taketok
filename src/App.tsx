import {createSignal} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";

function App() {

  async function readFromDb() {
    await invoke("read_from_db", {});
  }

  return (
    <div class="flex flex-col items-center max-w-full mt-7">
      <button
        class="rounded-3xl p-2 ps-4 pe-4 bg-purple-200"
        onClick={readFromDb}>Read from DB</button>
    </div>
  );
}

export default App;
