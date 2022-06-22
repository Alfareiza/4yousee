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
        assert len(response[0].keys()) == 7
        assert 'id' in response[0].keys()
        assert 'name' in response[0].keys()
        assert 'description' in response[0].keys()
        assert 'file' in response[0].keys()
        assert 'durationInSeconds' in response[0].keys()
        assert 'categories' in response[0].keys()
        assert 'schedule' in response[0].keys()
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_media_categories():
    """Test endpoint medias/categories"""

    response = client.get_media_category()
    assert isinstance(response, list)
    if response:
        assert len(response[0].keys()) == 9
        assert 'id' in response[0].keys()
        assert 'name' in response[0].keys()
        assert 'description' in response[0].keys()
        assert 'parent' in response[0].keys()
        assert 'children' in response[0].keys()
        assert 'carouselThumbnail' in response[0].keys()
        assert 'autoShuffle' in response[0].keys()
        assert 'updateFlow' in response[0].keys()
        assert 'sequence' in response[0].keys()
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_players():
    """Test endpoint players"""

    response = client.get_players()
    assert isinstance(response, list)
    if response:
        assert len(response[0].keys()) == 10
        assert 'id' in response[0].keys()
        assert 'name' in response[0].keys()
        assert 'description' in response[0].keys()
        assert 'platform' in response[0].keys()
        assert 'lastContactInMinutes' in response[0].keys()
        assert 'group' in response[0].keys()
        assert 'playerStatus' in response[0].keys()
        assert 'playlists' in response[0].keys()
        assert 'audios' in response[0].keys()
        assert 'lastLogReceived' in response[0].keys()
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_playlists():
    """Test endpoint playlists"""

    response = client.get_playlists()
    assert isinstance(response, list)
    if response:
        assert len(response[0].keys()) == 7
        assert 'id' in response[0].keys()
        assert 'name' in response[0].keys()
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
        assert len(response[0].keys()) == 5
        assert 'id' in response[0].keys()
        assert 'name' in response[0].keys()
        assert 'width' in response[0].keys()
        assert 'height' in response[0].keys()
        assert 'type' in response[0].keys()
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_newsources():
    """Test endpoint newsources"""

    response = client.get_newsources()
    assert isinstance(response, list)
    if response:
        assert len(response[0].keys()) == 11
        assert 'id' in response[0].keys()
        assert 'name' in response[0].keys()
        assert 'url' in response[0].keys()
        assert 'template' in response[0].keys()
        assert 'onlyWithImages' in response[0].keys()
        assert 'limit' in response[0].keys()
        assert 'daysToExpire' in response[0].keys()
        assert 'weight' in response[0].keys()
        assert 'variables' in response[0].keys()
        assert 'approveAutomatically' in response[0].keys()
        assert 'insertContentAutomatically' in response[0].keys()
    else:
        assert response == []


@vcr.use_cassette()
def test_retrieve_all_news():
    """Test endpoint newsources"""

    response = client.get_news()
    assert isinstance(response, list)
    if response:
        keys_response = response[0].keys()
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
        assert len(response[0].keys()) == 8
        assert 'id' in response[0].keys()
        assert 'type' in response[0].keys()
        assert 'format' in response[0].keys()
        assert 'filter' in response[0].keys()
        assert 'status' in response[0].keys()
        assert 'url' in response[0].keys()
        assert 'createdAt' in response[0].keys()
        assert 'updatedAt' in response[0].keys()
    else:
        assert response == []
