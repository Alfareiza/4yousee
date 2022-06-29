import pytest
import vcr

from tests import client


@vcr.use_cassette()
def test_retrieve_playlist_by_id():
    """Test endpoint playlist passing an id"""
    with pytest.raises(Exception):
        client.get_playlists(id=1_234)

    playlist_id_input = 1
    found_playlist_id = client.get_playlists(id=playlist_id_input)
    assert isinstance(found_playlist_id, dict)
    assert found_playlist_id.get('id') == playlist_id_input
