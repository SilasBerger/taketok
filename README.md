# README
## Setup
### Configuration
* The `taketok_home` directory is `%USERHOME%/.taketok` / `~/.taketok`
* Each config file is prefixed with `<configName>.` to support multiple configs. The run config can be specified as first argument, e.g. `taketok.py myConfig`
* The default config is named `default`

Create the default config file `default.config.json`
```json
{
  "videoOutputDir": "C:\\Users\\me\\path\\to\\taketok_out_dir",
  "importChunkSize": 5,
  "googleSheet": {
    "id": "Some Google Sheets sheet ID",
    "videoDataTab": "tiktokData"
  }
}
```

**Fields:**
* `videoOutputDir`: 
* `importChunkSize`: 
* `whisperModel`: `tiny` | `base` | `small` | `medium` | `large`
* `googleSheet.id`: 
* `googleSheet.videoDataTab`:

### Google Cloud Project
* Create a new Google Cloud project: https://console.cloud.google.com/projectcreate
* Activate Google Sheets API in that project: https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com
* Create OAuth credentials for that project: https://console.cloud.google.com/apis/credentials
  * Click Create Credentials > OAuth client ID
    * You may need to create a consent screen first. Just create a public consent screen, use default values everywhere, and add yourself as a test user.
  * Click Application type > Desktop app
  * In the Name field, type a name for the credential (e.g. `taketok`)
  * Confirm everything
  * Save the downloaded JSON file as `default.gcp-credentials.json` (or any config name other than `default`) in `taketok_home`

### Google Sheets Spreadsheet
* Create a Google Sheets spreadsheet with all tabs and columns required by `conf.json`, update values in `config.json` as needed
* Copy the spreadsheet ID from the Google Sheets URL (`https://docs.google.com/spreadsheets/d/<spreadsheet_id>/`) and update `googleSheet.id` in `conf.json` accordingly

### Python
* Install Python 3.10
* `python -m venv ./venv` (ensure Python version is 3.10)
* `source ./venv/bin/activate`
* `pip install -r requirements.txt`
* `python -m playwright install`
* `choco install ffmpeg` (Win) | `brew install ffmpeg` (MacOS) | `sudo apt install ffmpeg` (Debian)

### TODO
* Any formulas that need to be entered in a first row, to be automatically copied down
* Any source URLs that are needed as a seed
* Anything dynamic, such as a hashtag list used for crawling, etc.

## Troubleshooting
* When changing `scopes` in `conf.json`, delete the automatically generated `token.json` file

## Next Steps
* Append or integrate transcription step into current data pipeline (transcript should be independently retryable)
* Integrate OpenAI / GPT API

## Future Ideas
* Have a rating system for useful and not useful videos, use a simple ML model to learn best hashtags / users
* Google Sheets seeder: set up a blank Google sheet with the right schema
* Handle too many requests for Google Sheets
* Consider moving away from Google Sheets to Excel
* Dockerize

## Notes
* pip setup instructions for whisper didn't work, pip install command had to be `pip install git+https://github.com/openai/whisper.git`
* whisper didn't run on the latest Python version (3.11), had to use 3.10 (latest stable)