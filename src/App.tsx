import {onMount} from "solid-js";
import {invoke} from "@tauri-apps/api/tauri";
import "./App.css";
import PageCarousel from "./components/PageCarousel/PageCarousel";

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

  return ( <PageCarousel /> );
}

export default App;
