import json

import requests

from util.path_utils import taketok_home

source_links_file = taketok_home() / 'source-links.txt'
with open(source_links_file, "r") as infile:
    lines = [line.strip() for line in infile.readlines()]
    print(lines)

result = {
    'videoMetadata': [],
    'transcripts': []
}
imported_source_urls = []

for line in lines:
    print('Importing line %s' % line)

    import_response = requests.post('http://127.0.0.1:5000/import-from-source-url', json={
        'sourceUrl': line,
        'configName': 'dev'
    })

    if import_response.status_code != 200:
        continue

    metadata = import_response.json()
    video_id = metadata['video']['id']

    transcript_response = requests.post('http://127.0.0.1:5000/transcribe', json={
        'videoId': video_id,
        'configName': 'dev',
        'whisperModel': 'small'
    })

    if transcript_response.status_code != 200:
        continue

    result['videoMetadata'].append({
        'sourceUrl': line,
        'entry': metadata
    })
    result['transcripts'].append({
        'videoId': video_id,
        'entry': transcript_response.json()
    })
    imported_source_urls.append(line)

with open(taketok_home() / 'mock-data.json', "w") as outfile:
    json.dump(result, outfile, indent=2)

print(imported_source_urls)
