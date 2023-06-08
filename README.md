# TakeTok
A TikTok content distillery.

## Setup & Usage
**Note:** Whenever we mention the _taketok home_ or `~/taketok` directory, we refer to a directory called `taketok`,
located at the root of the user home, i.e. `~/taketok` (UNIX-like) or `%USERHOME%/taketok` (Windows). You will have to
create  this directory yourself, as part of the setup process.

**Note:** There is no support yet for saving TikTok links in the database. Until implemented, use the script
`db/insert_demo_data.sql`. The SQLite database file for the corresponding config is automatically created in the
_taketok home_ during the first run using that configuration.

### Step 1: Install the prerequisites
* **Python 3.10** - e.g. `brew install python@3.10` (macOS)
* **ffmpeg** - `brew install ffmpeg` (MacOS) | `choco install ffmpeg` (Win) | `sudo apt install ffmpeg` (Debian)

### Step 2: Set up the Python environment
Simply run `./setup.sh`

### Step 3: Create the configuration file
Configuration files tell `taketok` where to put and find stuff, and what to do. You can have multiple configuration
files for different use cases. All configuration files are located in `~/taketok/config`. The default configuration
file is `~/taketok/config/default.config.json`.

Create the default config file `~/taketok/config/default.config.json` as follows, for now:
```json
{
  "videoOutputDir": "/Users/me/path/to/where_i_want_my_videos",
  "whisperModel": "small"
}
```

**Here's what these fields mean:**
* `videoOutputDir`: Where `taketok` puts all downloaded videos
* `whisperModel`: The whisper transcription model to be used (`tiny` | `base` | `small` | `medium` | `large`)

### Step 4: Run it!
_With the virtual env activated (`source ./venv/bin/activate`)..._

* Run `python taketok.py` to launch `taketok` with the default config (`default.config.json`)
* Run `python taketok.py myOtherConfig` to launch `taketok` with a custom config called `myOtherConfig.config.json`

## Notes
* pip setup instructions for whisper didn't work, pip install command had to be `pip install git+https://github.com/openai/whisper.git`
* whisper didn't run on the latest Python version (3.11), had to use 3.10 (latest stable)