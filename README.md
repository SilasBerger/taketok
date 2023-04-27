# README
## Setup
### Configuration
* The `taketok` directory is located at `%USERHOME%/taketok` / `~/taketok`
* Each config and credential file is prefixed with `<configName>.` to support multiple configs. The run config can be
  specified as  first argument, e.g. `taketok.py myConfig`
* The default config is named `default`

Create the default config file `~/taketok/config/default.config.json`
```json
{
  "videoOutputDir": "C:\\Users\\me\\path\\to\\taketok_out_dir",
  "importBatchSize": 5,
  "googleSheet": {
    "id": "Some Google Sheets sheet ID",
    "videoDataTab": "tiktokData"
  }
}
```

**Fields:**
* `videoOutputDir`: Destination directory for downloaded videos
* `importBatchSize`: Number of video to be processed as single batch 
* `whisperModel`: Whisper transcription model to be used (`tiny` | `base` | `small` | `medium` | `large`)
* `googleSheet.id`: ID of the Google Sheet to be used
* `googleSheet.videoDataTab`: Name of the video data tab in that sheet

### Google Cloud Project
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

### Google Sheets Spreadsheet
* Create a Google Sheets spreadsheet
* Copy the spreadsheet ID from the Google Sheets URL (`https://docs.google.com/spreadsheets/d/<spreadsheet_id>/`) and
  update `googleSheet.id` in `<configName>.config.json` accordingly
* **TODO:** Set up spreadsheet according to layout, set video data tab name in config

### Python
* Install Python 3.10
* `python -m venv ./venv` (ensure Python version is 3.10)
* `source ./venv/bin/activate`
* `pip install -r requirements.txt`
* `python -m playwright install`
* `choco install ffmpeg` (Win) | `brew install ffmpeg` (MacOS) | `sudo apt install ffmpeg` (Debian)

## Notes
* pip setup instructions for whisper didn't work, pip install command had to be `pip install git+https://github.com/openai/whisper.git`
* whisper didn't run on the latest Python version (3.11), had to use 3.10 (latest stable)