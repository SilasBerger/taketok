import os.path
import random

from urllib.request import urlopen
from urllib.parse import urlparse
from TikTokApi import TikTokApi


class TikTokResult:

    def __init__(self, info, video_bytes):
        self.info = info
        self.bytes = video_bytes


def resolve_video_url_if_shortened(video_url: str) -> str:
    is_shortened = urlparse(video_url).netloc.startswith('vm.tiktok')
    return video_url if not is_shortened else urlopen(video_url).geturl()


def resolve_video_id(video_url: str) -> str:
    resolved_url = resolve_video_url_if_shortened(video_url)
    url_path = urlparse(resolved_url).path
    return os.path.split(url_path)[-1]


def tiktok_download(video_id: str) -> TikTokResult:
    did = str(random.randint(10000, 999999999))
    with TikTokApi(custom_device_id=did) as api:
        video = api.video(id=video_id)
        return TikTokResult(video.info_full(), video.bytes())
