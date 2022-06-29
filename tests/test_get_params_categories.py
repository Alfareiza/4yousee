import pytest
import vcr

from tests import client


@vcr.use_cassette()
def test_retrieve_media_categories_by_id():
    """Test endpoint media categories passing an id"""
    with pytest.raises(Exception):
        client.get_media_category(id=123_456)

    category_id_input = 1
    found_category_id = client.get_media_category(id=category_id_input)
    assert isinstance(found_category_id, dict)
    assert found_category_id.get('id') == category_id_input
