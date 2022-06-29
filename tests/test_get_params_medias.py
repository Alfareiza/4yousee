import pytest
import vcr

from tests import client


def test_retrieve_medias_by_id():
    """Test endpoint medias passing the id"""
    with pytest.raises(Exception):
        client.get_medias(id=123)

    id_input = 1
    existent_id = client.get_medias(id=id_input)
    assert isinstance(existent_id, dict)
    assert existent_id.get('id') == id_input


@vcr.use_cassette()
def test_retrieve_medias_by_name():
    """Test endpoint medias passing a name"""
    name_input = '4yousee'
    match_medias = client.get_medias(name=name_input)
    if match_medias:
        assert isinstance(match_medias, list)
    else:
        assert match_medias == []


@vcr.use_cassette()
def test_retrieve_medias_by_categoryId():
    """Test endpoint medias passing a categoryId"""
    category_id_input = 5
    found_category_id = client.get_medias(categoryId=category_id_input)
    if found_category_id:
        assert isinstance(found_category_id, list)
    else:
        assert found_category_id == []


@pytest.mark.parametrize('names', ['four yousee', '4yousee'])
@pytest.mark.parametrize('categories', [1, 1001])
def test_retrieve_medias_by_name_categoryId(names, categories):
    """Test endpoint medias passing multiple params"""
    match_media = client.get_medias(
        name=names,
        categoryId=categories
    )
    if match_media:
        assert isinstance(match_media, list)
    else:
        assert match_media == []
