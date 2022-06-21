import mimetypes
from pathlib import Path


def myme_type(file: Path) -> str:
    return mimetypes.guess_type(file)[0].replace(
        'application/x-zip-compressed', 'application/zip')


def filter_id(input_id, iterable):
    return list(filter(lambda i: i['id'] == input_id, iterable))
