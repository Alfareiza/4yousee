from tests import client


def test_edit_player_name():
    """Test endpoint put and passing the name"""
    name = 'Sample name via API'
    response = client.edit_player(id=2, name=name)
    assert response.get('name') == name


def test_edit_player_description():
    """Test endpoint put and passing only the description"""
    description = "Description from API"
    response = client.edit_player(id=2, description=description)
    assert response.get('description') == description


def test_edit_player_platform():
    """Test endpoint put and passing only the platform"""
    platform = 'SAMSUNG'
    response = client.edit_player(id=2, platform=platform)
    assert response.get('platform') == platform


def test_edit_player_group():
    """Test endpoint put and passing only the group"""
    group = 2
    response = client.edit_player(id=2, group=group)
    assert response.get('group')['id'] == group


def test_edit_player_playlists():
    """Test endpoint put and passing only the playlists"""
    id_plist = 1
    playlists = {'0': id_plist, '1': id_plist, '2': id_plist,
                 '3': id_plist, '4': id_plist, '5': id_plist,
                 '6': id_plist}

    response = client.edit_player(id=2, playlists=playlists)
    response_plist = {str(k): v['id'] for k, v in enumerate(
        list(response.get('playlists').values())
    )}
    assert response_plist == playlists


def test_edit_player_audios():
    """Test endpoint put and passing only the audios field"""
    audios = {"0": 1}
    response = client.edit_player(id=2, audios=audios)
    assert {'0': response['audios']['0']['id']} == audios
