import pytest
import vcr

from tests import client
from datetime import datetime
import random


# Resources for testing
def timestamp(input_data: str) -> float:
    try:
        return datetime.strptime(input_data, "%Y-%m-%d %H:%M:%S").timestamp()
    except ValueError:
        return datetime.strptime(input_data, "%Y-%m-%d").timestamp()


def random_idx(input: list) -> int:
    return random.randint(0, len(input) - 1)



@vcr.use_cassette()
def test_retrieve_news_by_newsourceId():
    """Test endpoint news passing an newsourceId"""
    new_newsourceId_input = 94
    match_news = client.get_news(newsourceId=new_newsourceId_input)
    if match_news:
        assert isinstance(match_news, list)
        assert match_news[
                   random_idx(match_news)
               ].get('newsourceId') == new_newsourceId_input
    else:
        assert match_news == []


@pytest.mark.parametrize('startDate',
                         ['2022-06-11 16:33:00',
                          '2022-06-30']
                         )
def test_retrieve_news_by_startDate(startDate):
    """Test endpoint news passing an startDate"""
    new_startDate_input = startDate
    match_news = client.get_news(startDate=new_startDate_input)
    if match_news:
        assert isinstance(match_news, list)
        assert timestamp(
            match_news[
                random_idx(match_news)
            ].get('startDate')
        ) >= timestamp(new_startDate_input)
    else:
        assert match_news == []


@pytest.mark.parametrize('endDate',
                         ['2021-01-01 16:33:00',
                          '2020-12-12',
                          '2010-01-01']
                         )
def test_retrieve_news_by_endDate(endDate):
    """Test endpoint news passing an endDate"""
    new_endDate_input = endDate
    match_news = client.get_news(endDate=new_endDate_input)
    if match_news:
        assert isinstance(match_news, list)
        assert timestamp(
            match_news[
                random_idx(match_news)
            ].get('endDate')
        ) >= timestamp(new_endDate_input)
    else:
        assert match_news == []


@pytest.mark.parametrize('startDate',
                         ['2022-05-01 08:30:00',
                          '2022-06-30',
                          '2005-12-31']
                         )
@pytest.mark.parametrize('endDate',
                         ['2022-05-31 20:58:00',
                          '2022-06-30',
                          '2005']
                         )
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
        assert timestamp(random_element.get('startDate')) \
               >= timestamp(new_startDate_input)
        assert timestamp(random_element.get('endDate')) \
               <= timestamp(new_endDate_input)
    else:
        assert match_news == []


@pytest.mark.parametrize('status',
                         ['approved',
                          'disapproved',
                          'waiting']
                         )
def test_retrieve_news_by_status(status):
    """Test endpoint news passing an status"""
    status_input = status
    match_news = client.get_news(status=status_input)
    if match_news:
        assert isinstance(match_news, list)
        assert match_news[
                   random_idx(match_news)
               ].get('status') == status_input
    else:
        assert match_news == []


@pytest.mark.parametrize('newsourceId', [94, 100, 51])
@pytest.mark.parametrize('status',
                         ['approved',
                          'disapproved',
                          'waiting'])
@pytest.mark.parametrize('startDate',
                         ['2022-01-01',
                          '2016-03-15 00:00:00',
                          '2022-12-31'])
@pytest.mark.parametrize('endDate',
                         ['2022-05-31 20:58:00',
                          '2022-06-30',
                          '2005'])
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
        assert timestamp(random_element.get('startDate')) \
               >= timestamp(startDate)
        assert timestamp(random_element.get('endDate'))\
               <= timestamp(endDate)
    else:
        assert match_news == []
