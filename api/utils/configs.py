import yaml


def get_filetypes():
    # Get the config definitions
    with open("config.yaml") as metadata:
        loader = yaml.load(metadata, Loader=yaml.FullLoader)
        audio_file_types = loader['audio-file-types']

    return audio_file_types


def get_configurations():
    # Get the config definitions
    with open("config.yaml") as metadata:
        loader = yaml.load(metadata, Loader=yaml.FullLoader)
        audio_file_types = loader['audio-file-types']
        song_required_fields = loader['song_required_fields']
        podcast_required_fields = loader['podcast_required_fields']
        audiobook_required_fields = loader['audiobook_required_fields']

    return audio_file_types, song_required_fields, podcast_required_fields, audiobook_required_fields
