# TakeTok
A TikTok content distillery.

## A quick word...
This project is under heavy construction 🚧. While the ultimate goal is of course to provide a simple, polished
out-of-the-box user experience for everyone, we are very much not there yet. Therefore, this setup guide and usage
instructions are solely targeted towards developers and other tech-savvy power users for now. It will get better ;)

## Setup
**Note:** Whenever we mention the _taketok home_ or `~/taketok` directory, we refer to a directory called `taketok`,
located at the root of the user home, i.e. `~/taketok` (UNIX-like) or `%USERHOME%/taketok` (Windows). You will have to
create  this directory yourself, as part of the setup process.

### Install the prerequisites
* **Python 3.10** - e.g. `brew install python@3.10` (macOS)
* **ffmpeg** - `brew install ffmpeg` (MacOS) | `choco install ffmpeg` (Win) | `sudo apt install ffmpeg` (Debian)
* **Rust** - `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

### Set up the Python environment (and some other useful stuff...)
Simply run `./setup.sh`

### Step 3: Create the configuration file
Configuration files tell `taketok` where to put and find stuff, and what to do. You can have multiple configuration
files for different use cases. All configuration files are located in `~/taketok/config`. The default configuration
file is `~/taketok/config/default.config.json`.

Create the default config file `~/taketok/config/default.config.json` as follows, for now:
```json
{
  "whisperModel": "small"
}
```

**Here's what these fields mean:**
* `whisperModel`: The whisper transcription model to be used (`tiny` | `base` | `small` | `medium` | `large`)

## Usage Instructions
_For all command line instructions in this section, make sure to have the virtualenv activated, which was previously
created for you by the `setup.sh` script (e.g. `source ./venv/bin/activate` for UNIX-like systems)._

### Importing source links
The starting point for the process of importing and transcribing videos is a list of source URLs - think of it as a
download queue. Until there is a full graphical UI, the easiest way to import source URLs is as follows:

Create a file `<taketok_home>/source-links.<config-name>.txt`, to which you can add any links to be imported into the
database, one link per line. Then, run the following command:

`python insert_source_links_from_file.py <config-name>`

from the `dev` directory, to go through this file and insert all links not yet present in the database corresponding to
the specified config. If no `<config-name>` is given, this will default to the `default` configuration as usual.

### Starting the API backend
The Python REST API backend is where all the core logic resides, when it comes to interacting with TikTok or
transcribing videos. This is also what will ultimately be left of the Python code, once the rest is migrated to
Tauri / Rust.

To launch the API backend, run the following command from the `src_python` directory:

`python -m flask --app taketok_api run`

### Launching the UI and importing videos
* ✅ You have completed the setup instructions, including creating the config file?
* ✅ You have imported some source links for your config of choice (e.g. `default`)?
* ✅ The REST API backend is running?

Great, you can now start importing videos!

To launch the UI, either use the `tauri dev` IntelliJ run config (or `tauri dev + reset` if you also want to reset
the database) or run `npm run tauri dev` from the command line.

### Some considerations
Currently, a lot of things are subject to change. So here are a few things to keep in mind:
* You may need to create file structure yourself, especially the DB file `taketok/data/default.sqlite`
* The mechanism for importing source links is subject to change and may break soon
* In `main.rs`, you can choose to either use the mock core API client or the real client. The mock client requires
  some external files that aren't currently checked in.

## Dev notes (this probably isn't particularly relevant to you...)
* pip setup instructions for whisper didn't work, pip install command had to be `pip install git+https://github.com/openai/whisper.git`
* whisper didn't run on the latest Python version (3.11), had to use 3.10 (latest stable)
* had to create a fork of TikTokApi (git+https://github.com/SilasBerger/TikTok-Api@41b507d9e04326dd20d86ae6c050ed54af4feef3)
  because there was an issue with the asyncio event loop, once I started using Flask