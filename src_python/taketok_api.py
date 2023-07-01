import asyncio
import traceback

from flask import Flask, request
from controller.data_import_controller import download_video
from transcribe.transcribe import transcribe_video
from util.path_utils import as_path

app = Flask(__name__)
asyncio.set_event_loop(asyncio.SelectorEventLoop())


@app.route('/import-from-source-url', methods=['POST'])
def import_from_source_url():
    payload = request.json
    try:
        source_url = payload['sourceUrl']
        video_out_dir = as_path(payload['videoOutputDir'])
        return download_video(source_url, video_out_dir), 200
    except Exception:
        return traceback.format_exc(), 500


@app.route('/transcribe', methods=['POST'])
def transcribe():
    payload = request.json
    video_id = payload['videoId']
    video_output_dir = as_path(payload['videoOutputDir'])
    whisper_model = payload['whisperModel']
    return transcribe_video(video_id, video_output_dir, whisper_model), 200
