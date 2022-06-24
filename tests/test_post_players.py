from tests import client


def test_post_player():
    """Test endpoint post and passing the required fields"""
    name = 'sample media player'
    playlists = {"0": 1, "1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1}
    platform = 'ANDROID'
    response = client.post_player(name=name, playlists=playlists, platform=platform)
    assert response.get('name') == name
    id_playlists = [i['id'] for i in response.get('playlists').values()]
    assert id_playlists == list(playlists.values())
    assert response.get('group').get('id') == 1
    assert response.get('platform') == platform
    client.delete_player(response.get('id'))
