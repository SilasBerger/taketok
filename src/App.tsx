import {createSignal} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = createSignal("");
  const [name, setName] = createSignal("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
    setGreetMsg(await invoke("greet", {name: name()}));
  }

  return (
    <div class="flex flex-col items-center max-w-full mt-7">
      <h1 class="text-5xl font-bold underline text-amber-500">
        Hello world!!
      </h1>

      <div class="mt-5 mb-5">
        <input
          class="border border-solid border-1 border-black mr-4 p-1 ps-3 pe-3 rounded-2xl"
          onChange={(e) => setName(e.currentTarget.value)}
          placeholder="Enter a name..."/>

        <button
          class="bg-blue-400 ps-4 pe-4 pt-2 pb-2 rounded-3xl"
          onClick={greet}>Greet</button>
      </div>

      <p>{greetMsg()}</p>
    </div>
  );
}

export default App;
