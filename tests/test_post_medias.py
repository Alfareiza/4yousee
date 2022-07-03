from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tests import client, BASE_DIR


def test_post_single_media_without_file():
    """Test endpoint post for medias"""
    with pytest.raises(Exception) as excinfo:
        client.add_media()
    assert str(excinfo.value) == 'Missing \'file\' field.'


def test_post_single_media_invalid_file():
    """Test endpoint posting an invalid file. An invalid file is a file
    that is not recognized by the 4yousee api"""
    with TemporaryDirectory() as temp:
        html_file = Path(temp) / "html_file.html"
        with html_file.open(mode="w+", encoding='cp850',
                            errors='replace') as ex_file:
            ex_file.write("<html><head></head><body></body></html>")
        with pytest.raises(Exception, match='Invalid file.'):
            client.add_media(file=str(html_file), categories=1)


def test_post_single_media_nonexistent_file():
    """Test endpoint post for an non existent file"""
    with pytest.raises(Exception, match='File not found.'):
        client.add_media(
            file="C:\\Users\\User\\Documents\\non-existent-file.mp4", categories=1)


def test_post_single_media_wmv():
    """Test endpoint post for an wmv file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-wmv-file.wmv'
    with pytest.raises(Exception, match='Invalid file.'):
        client.add_media(file=str(example_file), categories=1)


def test_post_single_media_mov():
    """Test endpoint post for an mov file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-mov-file.mov'
    with pytest.raises(Exception, match='Invalid file.'):
        client.add_media(file=str(example_file), categories=1)


def test_post_single_media_mp4():
    """Test endpoint post for an mp4 file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-mp4-file.mp4'
    response = client.add_media(file=str(example_file), categories=1)
    client.delete_media(response.get('id'))
    assert isinstance(response, dict)
    assert len(response.keys()) == 6
    assert response.get('name') == example_file.stem
    assert response.get('categories') == [1]


def test_post_single_media_zip():
    """Test endpoint post for an zip with duration"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-zip-file.zip'
    duration = 10
    response = client.add_media(file=str(example_file),
                                duration=duration, categories=1)
    client.delete_media(response.get('id'))
    assert isinstance(response, dict)
    assert len(response.keys()) == 6
    assert response.get('name') == example_file.stem
    assert response.get('categories') == [1]
    assert response.get('duration') == duration


def test_post_single_media_image_without_duration():
    """Test endpoint post for an image without duration"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    with pytest.raises(Exception,
                       match='Missing \'duration\' field. This must be an integer that '
                             'depicts the duration of the file in the playlist.'):
        client.add_media(file=example_file, categories=1)


def test_post_single_media_image_with_duration():
    """Test endpoint post for an image with duration"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    duration = 10
    response = client.add_media(file=str(example_file),
                                duration=duration, categories=1)
    client.delete_media(response.get('id'))
    assert isinstance(response, dict)
    assert len(response.keys()) == 6
    assert response.get('name') == example_file.stem
    assert response.get('categories') == [1]
    assert response.get('duration') == duration


def test_post_single_media_with_an_existent_category():
    """Test endpoint post for an image with an existent category."""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    response = client.add_media(file=str(example_file),
                                duration=10,
                                categories=[1])
    client.delete_media(response.get('id'))
    assert 1 in response.get('categories')


def test_post_single_media_with_an_non_existent_category():
    """Test endpoint post for an image with an non existent category."""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    category = 1_000
    with pytest.raises(Exception):
        client.add_media(file=str(example_file),
                         duration=10,
                         categories=category)


@pytest.mark.parametrize('category',
                         [
                             [3, 3_000, 1],
                             [1_000, 2_000, 3_000]
                         ])
def test_post_single_media_at_least_one_non_existent_in_multiple_categories(
        category):
    """Test endpoint post for an image with multiple categories where at least
    one of them doesn't exists in the 4yousee account."""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    with pytest.raises(Exception):
        client.add_media(file=str(example_file),
                         duration=10,
                         categories=category
                         )


@pytest.mark.parametrize('category',
                         [
                             [1, 2, 3],
                             [6, 7, 8]
                         ])
def test_post_single_media_all_existent_in_multiple_categories(category):
    """Test endpoint post for an image with multiple categories where all
      of them exists in the 4yousee account."""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    response = client.add_media(file=str(example_file),
                                duration=10,
                                categories=category
                                )
    client.delete_media(response.get('id'))
    assert category[0] in response.get('categories')
