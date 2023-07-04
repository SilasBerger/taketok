import {For, Setter} from "solid-js";
import {Page} from "../../shared/models";

function Navbar({setCurrentPage}: {setCurrentPage: Setter<Page>}) {
    return (
        <div class="w-full bg-amber-100 flex flex-row justify-stretch">
            <For each={Object.values(Page)}>{(page) =>
              <button onclick={() => setCurrentPage(page)}>{page}</button>
            }
            </For>
        </div>
    )
}

export default Navbar;