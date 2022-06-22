from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import vcr
from decouple import config

from fouryousee import FouryouseeAPI

TOKEN = config('TOKEN')
client = FouryouseeAPI(TOKEN)

BASE_DIR = Path(__file__).resolve().parent.parent


def test_post_upload_without_file():
    """Test endpoint for uploads without passin 'files' param"""
    with pytest.raises(Exception) as excinfo:
        client.upload_files(str())
    assert str(excinfo.value) == 'Missing \'files\' field.'


def test_post_upload_passing_str_path_file():
    """Test endpoint for uploads passing a str that
    depicts the path of an file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-mp4-file.mp4'
    response = client.upload_files(str(example_file))
    assert response[0].get('filename') == example_file.name


def test_post_upload_passing_list_of_str_path_files():
    """Test endpoint for uploads passing a list of str where
    every of them depicts the path of an file"""
    ex_file_one = BASE_DIR / 'tests/resources_for_tests/sample-mp4-file.mp4'
    ex_file_two = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    response = client.upload_files([str(i) for i in [ex_file_one, ex_file_two]])
    assert response[0].get('filename') == ex_file_one.name


def test_post_single_media_without_file():
    """Test endpoint post for medias"""
    with pytest.raises(Exception) as excinfo:
        client.post_single_media()
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
            client.post_single_media(file=str(html_file))


def test_post_single_media_nonexistent_file():
    """Test endpoint post for an non existent file"""
    with pytest.raises(Exception, match='File not found.'):
        client.post_single_media(
            file="C:\\Users\\User\\Documents\\non-existent-file.mp4")


def test_post_single_media_wmv():
    """Test endpoint post for an wmv file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-wmv-file.wmv'
    with pytest.raises(Exception, match='Invalid file.'):
        client.post_single_media(file=str(example_file))


def test_post_single_media_mov():
    """Test endpoint post for an mov file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-mov-file.mov'
    with pytest.raises(Exception, match='Invalid file.'):
        client.post_single_media(file=str(example_file))


@vcr.use_cassette()
def test_post_single_media_mp4():
    """Test endpoint post for an mp4 file"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-mp4-file.mp4'
    response = client.post_single_media(file=str(example_file))
    assert isinstance(response, dict)
    assert len(response.keys()) == 6
    assert response.get('name') == example_file.stem
    assert response.get('categories') == [1]


@vcr.use_cassette()
def test_post_single_media_zip():
    """Test endpoint post for an zip with duration"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-zip-file.zip'
    duration = 10
    response = client.post_single_media(file=str(example_file),
                                        duration=duration)
    assert isinstance(response, dict)
    assert len(response.keys()) == 6
    assert response.get('name') == example_file.stem
    assert response.get('categories') == [1]
    assert response.get('duration') == duration
    # Implement the next line
    # client.del_upload(response['id'])


@vcr.use_cassette()
def test_post_single_media_image_without_duration():
    """Test endpoint post for an image without duration"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    with pytest.raises(Exception,
                       match='Missing \'duration\' field. This must be an integer that '
                             'depicts the duration of the file in the playlist.'):
        client.post_single_media(file=example_file)


@vcr.use_cassette()
def test_post_single_media_image_with_duration():
    """Test endpoint post for an image with duration"""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    duration = 10
    response = client.post_single_media(file=str(example_file),
                                        duration=duration)
    assert isinstance(response, dict)
    assert len(response.keys()) == 6
    assert response.get('name') == example_file.stem
    assert response.get('categories') == [1]
    assert response.get('duration') == duration
    # Implement the next line
    # client.del_upload(response['id'])


@vcr.use_cassette()
def test_post_single_media_with_an_existent_category():
    """Test endpoint post for an image with an existent category."""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    category = 1
    response = client.post_single_media(file=str(example_file),
                                        duration=10,
                                        categories=1
                                        )
    assert category in response.get('categories')


@vcr.use_cassette()
def test_post_single_media_with_an_non_existent_category():
    """Test endpoint post for an image with an non existent category."""
    example_file = BASE_DIR / 'tests/resources_for_tests/sample-png-file.png'
    category = 1_000
    with pytest.raises(Exception) as excinfo:
        client.post_single_media(file=str(example_file),
                                 duration=10,
                                 categories=category
                                 )
    assert str(excinfo.value) == '{"message":"Category with ID ' + str(category) + ' was not found"}'


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
    with pytest.raises(Exception,
                       match=r'{"message":"Category with ID \d+ was not found"}'):
        client.post_single_media(file=str(example_file),
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
    response = client.post_single_media(file=str(example_file),
                                        duration=10,
                                        categories=category
                                        )
    assert category[0] in response.get('categories')
