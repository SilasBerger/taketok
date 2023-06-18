import os
import pathlib

import moviepy.editor
import whisper

from src.util.path_utils import tmp_dir
from src.util.config import Config


class VideoTranscriber:

    def __init__(self, config: Config):
        self._video_output_dir = config.video_output_dir
        self._model = config.whisper_model
        self._tmp_audio_file = str(tmp_dir() / 'tmp.mp3')

    def _extract_audio_tmp_file(self, video_id):
        print('Extracting audio from video %s' % video_id)
        video_file = str(self._video_output_dir / ('%s.mp4' % video_id))
        video = moviepy.editor.VideoFileClip(video_file)
        video.audio.write_audiofile(self._tmp_audio_file, verbose=False, logger=None)

    def _transcribe_audio(self) -> str:
        print('Transcribing video')
        model = whisper.load_model(self._model)
        return model.transcribe(self._tmp_audio_file)['text'].strip()

    def _remove_audio_tmp_file(self):
        file_path = pathlib.Path(self._tmp_audio_file)
        if not file_path.exists():
            return
        try:
            os.remove(file_path)
        except Exception:
            print('Unable to delete tmp audio file')

    def transcribe(self, video_id):
        self._extract_audio_tmp_file(video_id)
        try:
            transcript = self._transcribe_audio()
        except Exception as e:
            print(e)
            transcript = None
        self._remove_audio_tmp_file()
        return transcript
