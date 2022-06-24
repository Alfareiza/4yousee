from datetime import datetime
import random

import pytest
import vcr

# Resources for testing
from tests import client


def timestamp(input_data: str) -> float:
    try:
        return datetime.strptime(input_data, "%Y-%m-%d %H:%M:%S").timestamp()
    except ValueError:
        return datetime.strptime(input_data, "%Y-%m-%d").timestamp()


def random_idx(input: list) -> int:
    return random.randint(0, len(input) - 1)


# Follow the tests
@pytest.mark.parametrize('upload_id', ['123', '5021b3b7c402468d5b018a8b4a2b448a'])
def test_retrieve_upload_by_id(upload_id):
    """Test endpoint uploads passing an id"""
    match_upload = client.get_uploads('upload_id')
    if match_upload:
        assert isinstance(match_upload, dict)
        assert len(match_upload.keys()) == 2
        assert match_upload.get('id')
        assert match_upload.get('filename')
    else:
        assert match_upload == []


def test_retrieve_medias_by_id():
    """Test endpoint medias passing the id"""
    with pytest.raises(Exception):
        client.get_medias(id=123)

    id_input = 1
    existent_id = client.get_medias(id=id_input)
    assert isinstance(existent_id, dict)
    assert existent_id.get('id') == id_input


@vcr.use_cassette()
def test_retrieve_medias_by_name():
    """Test endpoint medias passing a name"""
    name_input = '4yousee'
    match_medias = client.get_medias(name=name_input)
    if match_medias:
        assert isinstance(match_medias, list)
    else:
        assert match_medias == []


@vcr.use_cassette()
def test_retrieve_medias_by_categoryId():
    """Test endpoint medias passing a categoryId"""
    category_id_input = 5
    found_category_id = client.get_medias(categoryId=category_id_input)
    if found_category_id:
        assert isinstance(found_category_id, list)
    else:
        assert found_category_id == []


@pytest.mark.parametrize('names', ['four yousee', '4yousee'])
@pytest.mark.parametrize('categories', [1, 1001])
def test_retrieve_medias_by_name_categoryId(names, categories):
    """Test endpoint medias passing multiple params"""
    match_media = client.get_medias(
        name=names,
        categoryId=categories
    )
    if match_media:
        assert isinstance(match_media, list)
    else:
        assert match_media == []


@vcr.use_cassette()
def test_retrieve_media_categories_by_id():
    """Test endpoint media categories passing an id"""
    with pytest.raises(Exception):
        client.get_media_category(id=123)

    category_id_input = 1
    found_category_id = client.get_media_category(category_id_input)
    assert isinstance(found_category_id, dict)
    assert found_category_id.get('id') == category_id_input


@vcr.use_cassette()
def test_retrieve_players_by_id():
    """Test endpoint players passing an id"""
    with pytest.raises(Exception):
        client.get_players(id=1_234)

    player_id_input = 1
    found_player_id = client.get_players(player_id_input)
    assert isinstance(found_player_id, dict)
    assert found_player_id.get('id') == player_id_input


@vcr.use_cassette()
def test_retrieve_playlist_by_id():
    """Test endpoint playlist passing an id"""
    with pytest.raises(Exception):
        client.get_playlists(id=1_234)

    playlist_id_input = 1
    found_playlist_id = client.get_playlists(playlist_id_input)
    assert isinstance(found_playlist_id, dict)
    assert found_playlist_id.get('id') == playlist_id_input


@vcr.use_cassette()
def test_retrieve_templates_by_id():
    """Test endpoint templates passing an id"""
    with pytest.raises(Exception):
        client.get_templates(id=1_234)

    template_id_input = 35
    found_template_id = client.get_templates(template_id_input)
    assert isinstance(found_template_id, dict)
    assert found_template_id.get('id') == template_id_input


@vcr.use_cassette()
def test_retrieve_news_by_newsourceId():
    """Test endpoint news passing an newsourceId"""
    new_newsourceId_input = 94
    match_news = client.get_news(newsourceId=new_newsourceId_input)
    if match_news:
        assert isinstance(match_news, list)
        assert match_news[random_idx(match_news)].get('newsourceId') \
               == new_newsourceId_input
    else:
        assert match_news == []


@pytest.mark.parametrize('startDate', ['2022-06-11 16:33:00', '2022-06-30'])
def test_retrieve_news_by_startDate(startDate):
    """Test endpoint news passing an startDate"""
    new_startDate_input = startDate
    match_news = client.get_news(startDate=new_startDate_input)
    if match_news:
        assert isinstance(match_news, list)
        assert timestamp(match_news[random_idx(match_news)].get('startDate')) \
               >= timestamp(new_startDate_input)
    else:
        assert match_news == []


@pytest.mark.parametrize('endDate',
                         ['2021-01-01 16:33:00', '2020-12-12', '2010-01-01'])
def test_retrieve_news_by_endDate(endDate):
    """Test endpoint news passing an endDate"""
    new_endDate_input = endDate
    match_news = client.get_news(endDate=new_endDate_input)
    if match_news:
        assert isinstance(match_news, list)
        assert timestamp(match_news[random_idx(match_news)].get('endDate')) \
               >= timestamp(new_endDate_input)
    else:
        assert match_news == []


@pytest.mark.parametrize('startDate',
                         ['2022-05-01 08:30:00', '2022-06-30', '2005-12-31'])
@pytest.mark.parametrize('endDate',
                         ['2022-05-31 20:58:00', '2022-06-30', '2005'])
def test_retrieve_news_by_startDate_endDate(startDate, endDate):
    """Test endpoint news passing an startDate and endDate"""
    new_startDate_input, new_endDate_input = startDate, endDate
    match_news = client.get_news(
        startDate=new_startDate_input,
        endDate=new_endDate_input
    )
    if match_news:
        assert isinstance(match_news, list)
        random_element = match_news[random_idx(match_news)]
        assert timestamp(random_element.get('startDate')) >= timestamp(
            new_startDate_input)
        assert timestamp(random_element.get('endDate')) <= timestamp(
            new_endDate_input)
    else:
        assert match_news == []


@pytest.mark.parametrize('status',
                         ['approved', 'disapproved', 'waiting'])
def test_retrieve_news_by_status(status):
    """Test endpoint news passing an status"""
    status_input = status
    match_news = client.get_news(status=status_input)
    if match_news:
        assert isinstance(match_news, list)
        assert match_news[random_idx(match_news)].get('status') == status_input
    else:
        assert match_news == []


@pytest.mark.parametrize('newsourceId', [94, 100, 51])
@pytest.mark.parametrize('status', ['approved', 'disapproved', 'waiting'])
@pytest.mark.parametrize('startDate',
                         ['2022-01-01', '2016-03-15 00:00:00', '2022-12-31'])
@pytest.mark.parametrize('endDate',
                         ['2022-05-31 20:58:00', '2022-06-30', '2005'])
def test_retrieve_news_by_newsourceId_status_startdate_enddate(newsourceId,
                                                               status,
                                                               startDate,
                                                               endDate):
    """Test endpoint news passing newsourceId, status, startDate and endDate"""
    match_news = client.get_news(newsourceId=newsourceId,
                                 status=status,
                                 startDate=startDate,
                                 endDate=endDate)
    if match_news:
        assert isinstance(match_news, list)
        random_element = match_news[random_idx(match_news)]
        assert len(random_element.keys()) == 11
        assert random_element.get('newsourceId') == newsourceId
        assert random_element.get('status') == status
        assert timestamp(random_element.get('startDate')) >= timestamp(
            startDate)
        assert timestamp(random_element.get('endDate')) <= timestamp(endDate)
    else:
        assert match_news == []


@vcr.use_cassette()
def test_retrieve_reports_by_id():
    """Test endpoint reports passing an id"""
    with pytest.raises(Exception):
        existent_id = client.get_reports(123_4567_890)

    existent_id = 158542
    match_report = client.get_reports(existent_id)
    if match_report:
        assert isinstance(match_report, dict)
        assert match_report.get('id') == existent_id
    else:
        assert match_report == []
