from tests import client


def test_post_reports():
    """Test endpoint post and passing the required fields"""

    filter = {
        "startDate": "2020-07-26",
        "startTime": "00:00:00",
        "endDate": "2020-08-24",
        "endTime": "23:59:59",
        "mediaId": [1, 2, 3],
        "playerId": [2],
        "sort": -1
    }
    response = client.request_report(filter=filter)
    assert response.get('filter').get('startDate') == filter['startDate']
    assert response.get('filter').get('startTime') == filter['startTime']
    assert response.get('filter').get('endDate') == filter['endDate']
    assert response.get('filter').get('endDate') == filter['endDate']
    assert response.get('filter').get('playerId') == filter['playerId']
