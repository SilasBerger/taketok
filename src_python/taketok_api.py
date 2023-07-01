import asyncio
import traceback

from flask import Flask, request
from data_importer import download_video
from util.path_utils import as_path


app = Flask(__name__)
asyncio.set_event_loop(asyncio.SelectorEventLoop())


@app.route('/import-from-source-url', methods=['POST'])
def import_from_source_url():
    payload = request.json

    if 'sourceUrl' not in payload:
        return 'Missing sourceUrl', 400
    if 'videoOutputDir' not in payload:
        return 'Missing videoOutputDir', 400

    try:
        source_url = payload['sourceUrl']
        video_out_dir = as_path(payload['videoOutputDir'])
        return download_video(source_url, video_out_dir), 200
    except Exception:
        return traceback.format_exc(), 500
