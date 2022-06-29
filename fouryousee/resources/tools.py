import mimetypes
from pathlib import Path
from typing import Dict, Any


def myme_type(file: Path) -> str:
    """Retorn mimetypes information"""
    return mimetypes.guess_type(file)[0].replace(
        'application/x-zip-compressed', 'application/zip')


def filter_id(input_id: str or int, iterable: list) -> list:
    """Filter a iterable accordding to an input id value"""
    return list(filter(lambda i: i['id'] == input_id, iterable))


def brief_player(player: dict) -> dict:
    """Receive a player object an return the information required
     to the payload """
    return dict(name=player['name'],
                description=player['description'],
                group=player['group']['id'],
                platform=player['platform'],
                playlists={str(k): v['id'] for k, v in
                           enumerate(player['playlists'].values())},
                audios={} if not player['audios']['0'] else {'0': player['audios']['0']['id']})


def brief_playlist(playlist: dict) -> dict:
    """Receive a playlist object an return the information required
     to the payload """
    return dict(name=playlist['name'],
                isSubPlaylist=playlist['isSubPlaylist'],
                category=playlist['category']['id'] if playlist['category'] else None,
                items=playlist['items'],
                sequence=playlist['sequence'])


def brief_media(media: dict) -> dict:
    """Receive a media object an return the information required
     to the payload """
    return dict(name=media['name'],
                duration=media['durationInSeconds'],
                categories=[i['id'] for i in media['categories']],
                schedule=media['schedule'])


def validate_kwargs_single_media(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_single_media function"""
    if not kwargs.get('file'):
        raise Exception('Missing \'file\' field.')

    if not kwargs.get('categories'):
        raise Exception('Missing \'categories\' field.')

    file = Path(kwargs.get('file'))
    if not file.exists():
        raise Exception('File not found.')
    mimetype = myme_type(file)
    type, extension = mimetype.split('/')
    if mimetype not in ['video/mp4',
                        'image/jpeg',
                        # 'image/gif',
                        'image/png',
                        'application/zip']:
        raise Exception('Invalid file.')
    if mimetype in ['image/jpeg', 'image/png', 'application/zip']:
        if not kwargs.get('duration'):
            raise Exception("Missing 'duration' field. This must "
                            "be an integer that depicts "
                            "the duration of the file in the playlist."
                            )
        elif not isinstance(kwargs.get('duration'), int):
            raise Exception('Invalid duration')
    if kwargs.get('category'):
        raise Exception('Invalid param must be \'categories\'.')


def validate_kwargs_single_media_category(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_media_category function"""
    if not kwargs.get('name'):
        raise Exception('Missing \'name\' field.')

    if parent := kwargs.get('parent'):
        if not isinstance(parent, int):
            raise Exception('Invalid parent, must be an integer')

    if shuffle := kwargs.get('autoShuffle'):
        if not isinstance(shuffle, bool):
            raise Exception('Invalid parent, must be True o False')

    if updateflow := kwargs.get('updateFlow'):
        if updateflow not in [1, 2]:
            raise Exception('Invalid updateFlow, must be 1 or 2')

    if sequence := kwargs.get('sequence'):
        if not isinstance(sequence, list):
            raise Exception('Invalid sequence, must be a list')


def validate_kwargs_player(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_player function"""

    if playlists := kwargs.get('playlists'):
        if not isinstance(playlists, dict) and \
                list(playlists.keys()) != ['0', '1', '2', '3', '4', '5', '6']:
            raise Exception('Invalid playlists field')

    if platform := kwargs.get('platform'):
        if not isinstance(platform, list) and \
                platform not in ['SAMSUNG', 'WINDOWS',
                                 'ANDROID', '4YOUSEE_PLAYER', 'LG']:
            raise Exception('Invalid platform field')

    if audios := kwargs.get('audios'):
        if not isinstance(audios, dict) and list(audios.keys()) != ['0']:
            raise Exception('Invalid audios field')


def validate_kwargs_playlist(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_playlists function"""
    if isSubPlaylist := kwargs.get('isSubPlaylist'):
        if not isinstance(isSubPlaylist, bool):
            raise Exception('Invalid isSubPlaylist field')

    if category := kwargs.get('category'):
        if not isinstance(category, int):
            raise Exception('Invalid category field')

    if items := kwargs.get('items'):
        if not isinstance(items, list):
            raise Exception('Invalid items field')

    if sequence := kwargs.get('sequence'):
        if not isinstance(sequence, list):
            raise Exception('Invalid sequences field')


def validate_kwargs_report(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_reports function"""
    if filter := kwargs.get('filter'):
        if not isinstance(filter, dict):
            raise Exception('Invalid audios field')

        if mediaId := kwargs.get('mediaId'):
            if not isinstance(mediaId, list):
                raise Exception('Invalid mediaId field')

        if playerId := kwargs.get('playerId'):
            if not isinstance(playerId, list):
                raise Exception('Invalid playerId field')
