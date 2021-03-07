import re
import yaml


# Get the config definitions
with open("config.yaml") as metadata:
    loader = yaml.load(metadata, Loader=yaml.FullLoader)
    audio_file_types = loader['audio-file-types']
    song_required_fields = loader['song_required_fields']
    podcast_required_fields = loader['podcast_required_fields']
    audiobook_required_fields = loader['audiobook_required_fields']


def validateAudioInput(audioFileType, audioFileMetadata):
    """    
    Desc: Validation for Audio Input
    Return: Errors Object
    """

    errors = {}

    # Validate entries

    if audioFileType.strip() == "":
        errors["audioFileType"] = "Audio file type is required"

    if audioFileMetadata == "" or audioFileMetadata == {}:
        errors["audioFileMetadata"] = "Audio file metadata is required"

    if audioFileType.strip() not in audio_file_types:
        errors["audioFileType"] = "Provide a valid audio file type"

    valid = len(errors) < 1

    return errors, valid


def validateSongMetadata(audioFileMetadata):
    """    
    Desc: Validation for Song Metadata Input
    Return: Errors Object
    """

    errors = {}

    # Validate entries

    if audioFileMetadata == "" or audioFileMetadata == {}:
        errors["audioFileMetadata"] = "Song file metadata is required"

    for key, value in audioFileMetadata.items():
        if key not in song_required_fields:
            errors["audioFileMetadata"] = "Song file metadata must have name of the song and duration"

        if str(value).strip() == "":
            errors["audioFileMetadata"] = f"Song file metadata must have a valid input"

    for field in song_required_fields:
        if field not in audioFileMetadata.keys():
            errors["audioFileMetadata"] = "Song file metadata must have name of the song and duration"

    valid = len(errors) < 1

    return errors, valid


def validatePodcastMetadata(audioFileMetadata):
    """    
    Desc: Validation for Podcast Metadata Input
    Return: Errors Object
    """

    errors = {}

    # Validate entries

    if audioFileMetadata == "" or audioFileMetadata == {}:
        errors["audioFileMetadata"] = "Podcast file metadata is required"

    for key, value in audioFileMetadata.items():
        if key not in podcast_required_fields:
            errors["audioFileMetadata"] = "Podcast file metadata must have name of the podcast, duration, host, and participants"

        if str(value).strip() == "":
            errors["audioFileMetadata"] = f"Podcast file metadata must have a valid input"

    for field in podcast_required_fields:
        if field not in audioFileMetadata.keys():
            errors["audioFileMetadata"] = "Podcast file metadata must have name of the podcast, duration, host, and participants"

    if type(audioFileMetadata['participants']) != list:
        errors["audioFileMetadata"] = "Invalid participants input"

    elif len(audioFileMetadata['participants']) > 10:
        errors["audioFileMetadata"] = "Maximum number of participants reached"

    valid = len(errors) < 1

    return errors, valid


def validateAudiobookMetadata(audioFileMetadata):
    """    
    Desc: Validation for Song Metadata Input
    Return: Errors Object
    """

    errors = {}

    # Validate entries

    if audioFileMetadata == "" or audioFileMetadata == {}:
        errors["audioFileMetadata"] = "Audiobook file metadata is required"

    for key, value in audioFileMetadata.items():
        if key not in audiobook_required_fields:
            errors["audioFileMetadata"] = "Audiobook file metadata must have title of the audiobook, duration, author of the title, and narrator"

        if str(value).strip() == "":
            errors["audioFileMetadata"] = f"Audiobook file metadata must have a valid input"

    for field in audiobook_required_fields:
        if field not in audioFileMetadata.keys():
            errors["audioFileMetadata"] = "Audiobook file metadata must have title of the audiobook, duration, author of the title, and narrator"

    valid = len(errors) < 1

    return errors, valid
