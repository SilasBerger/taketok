import os
import pathlib

import moviepy.editor
import whisper

from src_python.util.path_utils import tmp_dir, video_output_dir


def _extract_audio_tmp_file(video_id, video_output_dir, tmp_audio_file):
    print('Extracting audio from video %s' % video_id)
    video_file = str(video_output_dir / ('%s.mp4' % video_id))
    video = moviepy.editor.VideoFileClip(video_file)
    video.audio.write_audiofile(tmp_audio_file, verbose=False, logger=None)


def _transcribe_audio(tmp_audio_file, whisper_model_name) -> str:
    print('Transcribing video')
    model = whisper.load_model(whisper_model_name)
    return model.transcribe(tmp_audio_file)['text'].strip()


def _remove_audio_tmp_file(tmp_audio_file):
    file_path = pathlib.Path(tmp_audio_file)
    if not file_path.exists():
        return
    try:
        os.remove(file_path)
    except Exception:
        print('Unable to delete tmp audio file')


def transcribe_video(video_id, config_name, whisper_model):
    tmp_audio_file = str(tmp_dir() / 'tmp.mp3')
    video_output_dir_path = video_output_dir(config_name)
    _extract_audio_tmp_file(video_id, video_output_dir_path, tmp_audio_file)
    try:
        transcript = _transcribe_audio(tmp_audio_file, whisper_model)
    except Exception as e:
        print(e)
        transcript = None
    _remove_audio_tmp_file(tmp_audio_file)
    return transcript
