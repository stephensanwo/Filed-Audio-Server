# Audio File API for Filed.com

Audio File API, is an API that manages the file metadata of an Audio File Server

Three audio file types are supported:

- Song
- Podcast
- Audiobook

## Built with:

- Python 3.8
- Flask 1.1.2
- MongoDB
- Docker
- See full list of dependencies in requirements.txt

## Installation:

- clone the repository

  ```
  git clone >>>

  ```

- cd project/

- Create a virtual environment

  ```
  python3.8 -m venv env

  ```

- Activate the virtual environment

  ```
  source env/bin/activate

  ```

- Install the requirements

  ```
  pip install -r requirements.txt

  ```

- Run the application

  ```
  flask run

  ```

## Features:

### Application Security:

An API Key is created for the API using the api-credentials CLI tool. An API Key is required on specific routes. See URL endpoints below for details.

To generate an API. in the CLI, run:

```
python api-credentials.py john.doe@email.com

```

### Event Logging

### Application Features:

### URL endpoints

| URL Endpoint                                                                 | HTTP Methods | Summary                                                                       |
| ---------------------------------------------------------------------------- | ------------ | ----------------------------------------------------------------------------- |
| `api/create`                                                                 | `POST`       | Creates a new Audio File Record                                               |
| `api/get_audio_file?audioFileType=<audioFileType>`                           | `GET`        | Retrieves all Audio Files for a specific file type (song, podcast, audiobook) |
| `api/get_audio_file?audioFileType=<audioFileType>&audioFileID=<audioFileID>` | `GET`        | Retrieves a specific Audio File by file type and file ID                      |

#### Example -> Create New Song

```
Example body
{
    "audioFileType": "song",
    "audioFileMetadata": {
        "name_of_song": "Paradise, Coldplay",
        "duration": 40
    }
}
```

#### Example -> Create New Podcast

```
{
    "audioFileType": "podcast",
    "audioFileMetadata": {
        "name_of_podcast": "All In Podcast",
        "duration": 1909,
        "host": "Jason Calacanis",
        "participants": ["Chamath Palihapitiya", "Davis Sacks","David Friedberg"]
    }
}
```

#### Example -> Create New Podcast

```
{
    "audioFileType": "podcast",
    "audioFileMetadata": {
        "name_of_podcast": "All In Podcast",
        "duration": 1909,
        "host": "Jason Calacanis",
        "participants": ["Chamath Palihapitiya", "Davis Sacks","David Friedberg"]
    }
}
```

#### Example -> Create New Audiobook

```
{
    "audioFileType": "audiobook",
    "audioFileMetadata": {
        "title_of_audiobook": "Born a Crime",
        "author_of_title": "Trevor Noah",
        "narrator": "Trevor Noah",
        "duration": 390492
    }
}
```

## Deployement

### Todos

## License

MIT

## Author

[Stephen Sanwo](https://github.com/stephensanwo)
