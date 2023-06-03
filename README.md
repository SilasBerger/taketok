# TakeTok
A TikTok content distillery.

## Setup Instructions
**Note:** Whenever we mention the _taketok home_ or `~/taketok` directory, we refer to a directory called `taketok`,
located at the root of the user home, i.e. `~/taketok` (UNIX-like) or `%USERHOME%/taketok`. You will have to create
this directory yourself, as part of the setup process.

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
  "importBatchSize": 3,
  "whisperModel": "small",
  "googleSheet": {
    "id": "",
    "videoDataTab": ""
  }
}
```

**Here's what these fields mean:**
* `videoOutputDir`: Where `taketok` put all downloaded videos
* `importBatchSize`: How many videos should be processed as a batch before saving to Google Sheets
* `whisperModel`: The whisper transcription model to be used (`tiny` | `base` | `small` | `medium` | `large`)
* `googleSheet.id`: ID of the Google Sheet to be used (you can leave this empty until step 5)
* `googleSheet.videoDataTab`: Name of the video data tab in that sheet (can also be empty until step 5)

### Step 4: Set up a GCP project for Google Sheets API access
* Create a new Google Cloud project: https://console.cloud.google.com/projectcreate
* Activate Google Sheets API in that project: https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com
* Create OAuth credentials for that project: https://console.cloud.google.com/apis/credentials
  * Click Create Credentials > OAuth client ID
    * You may need to create a consent screen first. Just create a public consent screen, use default values everywhere,
      and add yourself as a test user.
  * Click Application type > Desktop app
  * In the Name field, type a name for the credential (e.g. `taketok`)
  * Confirm everything
  * Save the downloaded JSON file as `default.gcp-credentials.json` (or any config name other than `default`) in
    `~/taketok/config`

### Step 5: Create a Google Sheets spreadsheet
* Create a Google Sheets spreadsheet
* Copy the spreadsheet ID from the Google Sheets URL (`https://docs.google.com/spreadsheets/d/<spreadsheet_id>/`) and
  update `googleSheet.id` in `<configName>.config.json` accordingly
* Name the spreadsheet tab where `taketok` should work, and copy this name to `googleSheet.videoDataTab`
* **TODO:** Spreadsheet layout

### Step 6: Run it!
_With the virtual env activated (`source ./venv/bin/activate`)..._

* Run `python taketok.py` to launch `taketok` with the default config (`default.config.json`)
* Run `python taketok.py myOtherConfig` to launch `taketok` with a custom config called `myOtherConfig.config.json`

## Notes
* pip setup instructions for whisper didn't work, pip install command had to be `pip install git+https://github.com/openai/whisper.git`
* whisper didn't run on the latest Python version (3.11), had to use 3.10 (latest stable)