import datetime
import pathlib

from src_python.tiktok.tiktok import resolve_video_id, tiktok_download, resolve_video_url_if_shortened


def _save_video(video_bytes, video_id, video_out_dir):
    filename = video_out_dir / ('%s.mp4' % video_id)
    with open(filename, 'wb') as video_outfile:
        video_outfile.write(video_bytes)


def _extract_hashtags(info):
    return [hashtag['hashtagName'] for hashtag in info['textExtra']] if 'textExtra' in info else []


def _extract_challenges(info):
    return [{
        "id": challenge["id"],
        "title": challenge["title"],
        "description": challenge["desc"],
    } for challenge in info["challenges"]] if "challenges" in info else []


def download_video(source_url: str, video_out_dir: pathlib.Path):
    current_date_iso = datetime.datetime.now().isoformat()  # TODO: Use UTC date
    resolved_url = resolve_video_url_if_shortened(source_url)
    video_id = resolve_video_id(resolved_url)

    tiktok_result = tiktok_download(video_id)
    _save_video(tiktok_result.bytes, video_id, video_out_dir)

    info = tiktok_result.info['itemInfo']['itemStruct']
    author = info['author']

    return {
        'video': {
            "id": video_id,
            "resolvedUrl": resolved_url,
            "downloadDateIso": current_date_iso,
            "description": info['desc'],
            "uploadDateIso": datetime.datetime.utcfromtimestamp(info['createTime']).isoformat(),
            'hashtags': _extract_hashtags(info),
            'challenges': _extract_challenges(info)
        },
        'author': {
            "id": author['id'],
            'uniqueId': author['uniqueId'],
            'nickname': author['nickname'],
            'signature': author['signature'],
            'date': current_date_iso
        }
    }
