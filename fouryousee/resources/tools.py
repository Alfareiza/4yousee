import mimetypes
from pathlib import Path


def myme_type(file: Path) -> str:
    """Retorn mimetypes information"""
    return mimetypes.guess_type(file)[0].replace(
        'application/x-zip-compressed', 'application/zip')


def filter_id(input_id: str or int, iterable: list) -> list:
    """Filter a iterable accordding to an input id value"""
    return list(filter(lambda i: i['id'] == input_id, iterable))


def validate_kwargs_single_media(**kwargs) -> Exception or None:
    """Validate the kwargs sent to the post_single_media function"""
    if not kwargs.get('file'):
        raise Exception('Missing \'file\' field.')
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
