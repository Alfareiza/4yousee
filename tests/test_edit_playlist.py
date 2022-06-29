from tests import client


def test_edit_playlist_name():
    """Test endpoint put and passing the name"""
    name = 'Sample name via API'
    response = client.edit_playlist(id=70, name=name)
    assert response.get('name') == name


def test_edit_playlist_category():
    """Test endpoint put and passing only the category"""
    category = 1
    response = client.edit_playlist(id=70, category=category)
    assert response.get('category').get('id') == category


def test_edit_playlist_isSubPlaylist():
    """Test endpoint put and passing only the isSubPlaylist"""
    response = client.edit_playlist(id=70, isSubPlaylist=True)
    assert bool(response.get('isSubPlaylist'))
