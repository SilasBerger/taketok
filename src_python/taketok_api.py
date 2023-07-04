import traceback
import json

from flask import Flask, request
from controller.data_import_controller import download_video
from transcribe.transcribe import transcribe_video
from util.path_utils import as_path

app = Flask(__name__)


@app.route('/import-from-source-url', methods=['POST'])
def import_from_source_url():
    payload = request.json
    try:
        source_url = payload['sourceUrl']
        video_out_dir = as_path(payload['videoOutputDir'])
        response = download_video(source_url, video_out_dir)
        print(json.dumps({"source_url": source_url, "response": response}, indent=2))
        return response, 200
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        return stack_trace, 500


@app.route('/transcribe', methods=['POST'])
def transcribe():
    payload = request.json
    video_id = payload['videoId']
    video_output_dir = as_path(payload['videoOutputDir'])
    whisper_model = payload['whisperModel']
    transcript = transcribe_video(video_id, video_output_dir, whisper_model)
    response = {'transcript': transcript}
    print(json.dumps({"video_id": video_id, "response": response}, indent=2))
    return response, 200
