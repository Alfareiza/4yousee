import vcr

from fouryousee import FouryouseeAPI
from decouple import config

TOKEN = config('TOKEN')
client = FouryouseeAPI(TOKEN)


@vcr.use_cassette()
def test_retrieve_all_users():
    """Test endpoint users"""
    response = client.get_users()

    assert isinstance(response, list)
    assert len(response[0].keys()) == 5
    assert response[0].get('id', False)
    assert response[0].get('name', False)
    assert response[0].get('username', False)
    assert response[0].get('email', False)
    assert response[0].get('group', False)
    assert response[0].get('group', False).get('id', False)
    assert response[0].get('group', False).get('name', False)


@vcr.use_cassette()
def test_retrieve_all_users_groups():
    """Test endpoint users/groups"""

    response = client.get_users_groups()
    assert isinstance(response, list)
    assert len(response[0].keys()) == 3
    assert response[0].get('id', False)
    assert response[0].get('name', False)
    assert response[0].get('description', False)


@vcr.use_cassette()
def test_retrieve_all_uploads():
    """Test endpoint uploads"""

    response = client.get_uploads()
    assert isinstance(response, list)
    if response:
        assert len(response[0].keys()) == 2
        assert response[0].get('id', False)
        assert response[0].get('filename', False)
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_medias():
    """Test endpoint medias"""

    response = client.get_medias()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(keys_response) == 7
        assert 'id' in keys_response
        assert 'name' in keys_response
        assert 'description' in keys_response
        assert 'file' in keys_response
        assert 'durationInSeconds' in keys_response
        assert 'categories' in keys_response
        assert 'schedule' in keys_response
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_media_categories():
    """Test endpoint medias/categories"""

    response = client.get_media_category()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(response[0].keys()) == 9
        assert 'id' in keys_response
        assert 'name' in keys_response
        assert 'description' in keys_response
        assert 'parent' in keys_response
        assert 'children' in keys_response
        assert 'carouselThumbnail' in keys_response
        assert 'autoShuffle' in keys_response
        assert 'updateFlow' in keys_response
        assert 'sequence' in keys_response
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_players():
    """Test endpoint players"""

    response = client.get_players()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(keys_response) == 10
        assert 'id' in keys_response
        assert 'name' in keys_response
        assert 'description' in keys_response
        assert 'platform' in keys_response
        assert 'lastContactInMinutes' in keys_response
        assert 'group' in keys_response
        assert 'playerStatus' in keys_response
        assert 'playlists' in keys_response
        assert 'audios' in keys_response
        assert 'lastLogReceived' in keys_response
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_playlists():
    """Test endpoint playlists"""

    response = client.get_playlists()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(keys_response) == 7
        assert 'id' in keys_response
        assert 'name' in keys_response
        assert 'durationInSeconds' in response[0].keys()
        assert 'isSubPlaylist' in response[0].keys()
        assert 'category' in response[0].keys()
        assert 'items' in response[0].keys()
        assert 'sequence' in response[0].keys()
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_templates():
    """Test endpoint templates"""

    response = client.get_templates()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(keys_response) == 5
        assert 'id' in keys_response
        assert 'name' in keys_response
        assert 'width' in keys_response
        assert 'height' in keys_response
        assert 'type' in keys_response
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_newsources():
    """Test endpoint newsources"""

    response = client.get_newsources()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(keys_response) == 11
        assert 'id' in keys_response
        assert 'name' in keys_response
        assert 'url' in keys_response
        assert 'template' in keys_response
        assert 'onlyWithImages' in keys_response
        assert 'limit' in keys_response
        assert 'daysToExpire' in keys_response
        assert 'weight' in keys_response
        assert 'variables' in keys_response
        assert 'approveAutomatically' in keys_response
        assert 'insertContentAutomatically' in keys_response
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_news():
    """Test endpoint newsources"""

    response = client.get_news()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(keys_response) == 10
        assert 'id' in keys_response
        assert 'content' in keys_response
        assert 'file' in keys_response
        assert 'creationDate' in keys_response
        assert 'approvalDate' in keys_response
        assert 'status' in keys_response
        assert 'startDate' in keys_response
        assert 'endDate' in keys_response
        assert 'newsourceId' in keys_response
        assert 'newsourceName' in keys_response
        assert 'image' in keys_response
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_reports():
    """Test endpoint reports"""

    response = client.get_reports()
    assert isinstance(response, list)
    if response:
        keys_response = list(response[0].keys())
        assert len(response[0].keys()) == 8
        assert 'id' in keys_response
        assert 'type' in keys_response
        assert 'format' in keys_response
        assert 'filter' in keys_response
        assert 'status' in keys_response
        assert 'url' in keys_response
        assert 'createdAt' in keys_response
        assert 'updatedAt' in keys_response
    else:
        assert response == []
