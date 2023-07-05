import {Accessor, For, Setter} from "solid-js";
import {Page} from "../../shared/models";

function Navbar({currentPage, setCurrentPage}: {currentPage: Accessor<Page>, setCurrentPage: Setter<Page>}) {
    return (
        <div class="fixed z-40 w-full bg-gray-100 bg-opacity-90 backdrop-blur-md
                    flex flex-row justify-stretch">
            <For each={Object.values(Page)}>{(page) =>
              <button
                class={`px-6 py-3
                        text-xl font-bold
                        hover:bg-gray-200 ${page == currentPage() ? 'bg-gray-200' : ''}
                        transition-all`}
                onclick={() => setCurrentPage(page)}>{page}</button>
            }
            </For>
        </div>
    )
}

export default Navbar;