import mimetypes
from pathlib import Path


def myme_type(file: Path) -> str:
    return mimetypes.guess_type(file)[0].replace(
        'application/x-zip-compressed', 'application/zip')


def filter_id(input_id, iterable):
    return list(filter(lambda i: i['id'] == input_id, iterable))


def validate_kwargs_single_media(**kwargs):
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
