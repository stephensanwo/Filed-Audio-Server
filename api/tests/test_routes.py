import json


def get_audio_files(api, client):
    del api
    res = client.get('/api/v1/get_audio_files')
    assert res.status_code == 200
