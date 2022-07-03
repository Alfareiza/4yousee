from tests import client


def test_post_media_category_passing_name():
    """Test endpoint post for an media category passing only the name"""
    name = 'sample media category'
    response = client.add_media_category(name=name)
    assert response.get('name') == name


def test_post_media_category_passing_parent():
    """Test endpoint post for an media category passing
      the name and the parent"""
    name = 'sample media category'
    parent = 1
    response = client.add_media_category(name=name, parent=parent)
    assert response.get('parent').get('id') == parent


def test_post_media_category_passing_shuffle():
    """Test endpoint post for an media category passing
      the name and parent'"""
    name = 'sample media category'
    parent = 1
    autoShuffle = True
    response = client.add_media_category(name=name,
                                         parent=parent,
                                         autoShuffle=autoShuffle)
    assert response.get('autoShuffle') == autoShuffle


def test_post_media_category_passing_updateflow():
    """Test endpoint post for an media category passing
      the name, parent and shuffle"""
    name = 'sample media category'
    parent = 1
    shuffle = True
    updateflow = 2
    response = client.add_media_category(name=name,
                                         parent=parent,
                                         shuffle=shuffle,
                                         updateFlow=updateflow)
    assert response.get('updateFlow') == str(updateflow)
