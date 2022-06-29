import pytest
import vcr

from tests import client


@vcr.use_cassette()
def test_retrieve_players_by_id():
    """Test endpoint players passing an id"""
    with pytest.raises(Exception):
        client.get_players(id=1_234)

    player_id_input = 1
    found_player_id = client.get_players(id=player_id_input)
    assert isinstance(found_player_id, dict)
    assert found_player_id.get('id') == player_id_input
