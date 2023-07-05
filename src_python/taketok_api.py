import traceback
import json

from flask import Flask, request, send_file
from controller.data_import_controller import download_video
from transcribe.transcribe import transcribe_video
from util.path_utils import as_path, video_output_dir, thumbnails_dir

app = Flask(__name__)


@app.route('/import-from-source-url', methods=['POST'])
def import_from_source_url():
    payload = request.json
    try:
        source_url = payload['sourceUrl']
        config_name = payload['configName']
        response = download_video(source_url, config_name)
        return response, 200
    except Exception:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        return stack_trace, 500


@app.route('/transcribe', methods=['POST'])
def transcribe():
    payload = request.json
    video_id = payload['videoId']
    configName = as_path(payload['configName'])
    whisper_model = payload['whisperModel']
    transcript = transcribe_video(video_id, configName, whisper_model)
    response = {'transcript': transcript}
    return response, 200


@app.route('/video/<config_name>/<video_id>')
def serve_video(config_name, video_id):
    video_file = video_output_dir(config_name) / ('%s.mp4' % video_id)
    return send_file(str(video_file))


@app.route('/thumbnail/<config_name>/<video_id>')
def serve_thumbnail(config_name, video_id):
    video_file = thumbnails_dir(config_name) / ('%s.jpg' % video_id)
    return send_file(str(video_file))
