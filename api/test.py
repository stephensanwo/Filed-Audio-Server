import json
import unittest
from flask import Flask
from api import api
from database.AudioSchema import Song, Podcast, Audiobook


# Define test data
headers = dict(api_key="2c5a16d9-a951-4f62-ac68-e4df97e7b15d",
               api_client="jane.doe@email.com"
               )

# Change ID on run
podcastTestID = "6046fcc995184fd26e82cac1"
songTestID = "60471b3a669529b65c5ffb72"
audiobookTestID = "60470a51b95704ef06d9925c"

test_song = {
    "audioFileType": "song",
    "audioFileMetadata": {
        "name_of_song": "Paradise by Coldplay",
        "duration": 40
    }
}

test_podcast = {
    "audioFileType": "podcast",
    "audioFileMetadata": {
        "name_of_podcast": "Loose Talk",
        "duration": 1909,
        "host": "AOT2",
        "participants": ["AOT2", "Bad Girl Mo", "Jess Jess Finess", "Steve Dede Canada"]
    }
}
test_audiobook = {
    "audioFileType": "audiobook",
    "audioFileMetadata": {
        "title_of_audiobook": "Born a Crime",
        "author_of_title": "Trevor Noah",
        "narrator": "Trevor Noah",
        "duration": 390492
    }
}


class APITest(unittest.TestCase):

    def setUp(self):
        self.api = api.test_client()
        songDB = Song()
        podcastDB = Podcast()
        audiobookDB = Audiobook()

    # Test Create Audio files

    def test_create_song(self):

        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=headers,
            data=json.dumps(test_song))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_create_podcast(self):

        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=headers,
            data=json.dumps(test_podcast))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_create_audiobook(self):

        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=headers,
            data=json.dumps(test_audiobook))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    # Test API Key

    def test_create_song_with_wrong_api_key(self):
        wrong_headers = dict(api_key="4c5a16d9-a951-4f62-ac68-e4df97e7b15d",
                             api_client="jane.doe@email.cox"
                             )
        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=wrong_headers,
            data=json.dumps(test_song))

        self.assertEqual(response.status_code, 401)

    # Test wrong data input

    def test_create_song_with_wrong_data(self):
        song = {
            "audioFileType": "song",
            "audioFileMetadata": {
                "name_of_song": "",
                "duration": ""
            }
        }
        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=headers,
            data=json.dumps(song))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_create_podcast_with_wrong_data(self):
        podcast = {
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "name_of_podcast": "",
                "duration": "",
                "host": "",
                "participants": ""
            }
        }
        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=headers,
            data=json.dumps(podcast))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_create_audiobook(self):
        audiobook = {
            "audioFileType": "audiobook",
            "audioFileMetadata": {
                "title_of_audiobook": "",
                "author_of_title": "",
                "narrator": "",
                "duration": ""
            }
        }
        response = self.api.post(
            'api/v1/create', content_type="application/json",
            headers=headers,
            data=json.dumps(audiobook))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

   # Test the Get all audio file routes

    def test_if_can_get_all_songs(self):
        response = self.api.get('api/v1/get_audio_files?audioFileType=song')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        self.assertTrue(type(data['data']['songs'] == list))

    def test_if_can_get_all_podcasts(self):
        response = self.api.get('api/v1/get_audio_files?audioFileType=podcast')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        self.assertTrue(type(data['data']['podcasts'] == list))

    def test_if_can_get_all_audiobooks(self):
        response = self.api.get(
            'api/v1/get_audio_files?audioFileType=audiobook')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        self.assertTrue(type(data['data']['audiobooks'] == list))

    # Test the Get single audio file by audioFileID routes

    def test_if_can_get_song_by_id(self):
        response = self.api.get(
            f'api/v1/get_audio_file?audioFileType=song&audioFileID={songTestID}')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_if_can_get_podcast_by_id(self):
        response = self.api.get(
            f'api/v1/get_audio_file?audioFileType=podcast&audioFileID={podcastTestID}')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_if_can_get_audibook_by_id(self):
        response = self.api.get(
            f'api/v1/get_audio_file?audioFileType=audiobook&audioFileID={audiobookTestID}')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    # Test the update audio file routes

    def test_if_can_update_song(self):
        response = self.api.post(
            f'api/v1/update_audio_file?audioFileType=song&audioFileID={songTestID}', content_type="application/json", headers=headers, data=json.dumps(test_song))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_if_can_update_podcast(self):
        response = self.api.post(
            f'api/v1/update_audio_file?audioFileType=podcast&audioFileID={podcastTestID}', content_type="application/json", headers=headers, data=json.dumps(test_podcast))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_if_can_update_audiobook(self):
        response = self.api.post(
            f'api/v1/update_audio_file?audioFileType=podcast&audioFileID={podcastTestID}', content_type="application/json", headers=headers, data=json.dumps(test_podcast))

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    # Test the delete audio file routes

    def test_if_can_delete_song(self):
        response = self.api.post(
            f'api/v1/delete_audio_file?audioFileType=song&audioFileID={songTestID}', headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_if_can_delete_podcast(self):
        response = self.api.post(
            f'api/v1/delete_audio_file?audioFileType=podcast&audioFileID={podcastTestID}')

        self.assertEqual(response.status_code, 200)

    def test_if_can_delete_audiobook(self):
        response = self.api.post(
            f'api/v1/delete_audio_file?audioFileType=audiobook&audioFileID={audiobookTestID}')

        self.assertEqual(response.status_code, 200)

    # Test the database models

    def test_create_song(self):
        song = Song(name_of_song="Paradise by Coldplay Now", duration=40)
        song_data = song.song_data()
        assert song_data['name_of_song'] == "Paradise by Coldplay Now"
        assert song_data['duration'] == 40

    def test_create_podcast(self):
        podcast = Podcast(name_of_podcast="All In Podcast", duration=1909, host="Jason Calacanis",
                          participants=["Chamath Palihapitiya", "Davis Sacks", "David Friedberg"])

        podcast_data = podcast.podcast_data()
        assert podcast_data['name_of_podcast'] == "All In Podcast"
        assert podcast_data['duration'] == 1909
        assert podcast_data['host'] == "Jason Calacanis"
        assert podcast_data['participants'] == [
            "Chamath Palihapitiya", "Davis Sacks", "David Friedberg"]

    def test_create_audiobook(self):
        """
        Desc: Test that the fields are correctly defined in the model
        """
        audiobook = Audiobook(title_of_audiobook="Born a Crime", duration=390492, author_of_title="Trevor Noah",
                              narrator="Trevor Noah")

        audiobook_data = audiobook.audiobook_data()
        assert audiobook_data['title_of_audiobook'] == "Born a Crime"
        assert audiobook_data['duration'] == 390492
        assert audiobook_data['author_of_title'] == "Trevor Noah"
        assert audiobook_data['narrator'] == "Trevor Noah"

    """
    Desc: Test DB connections
    """

    def test_db_connection(self):
        songDB = Song()
        podcastDB = Podcast()
        audiobookDB = Audiobook()

        self.assertTrue(songDB)
        self.assertTrue(podcastDB)
        self.assertTrue(audiobookDB)

    def tearDown(self):
        songDB = Song()
        podcastDB = Podcast()
        audiobookDB = Audiobook()


if __name__ == "__main__":
    unittest.main()
