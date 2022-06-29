from tests import client


def test_edit_media_name():
    """Test endpoint put and passing only the name"""
    name = 'Sample name via API'
    response = client.edit_media(id=230, name=name)
    assert response.get('name') == name


def test_edit_media_categories():
    """Test endpoint put and passing only the category(ies)"""
    categories = [11, 12, 13]
    response = client.edit_media(id=230, categories=categories)
    assert response.get('categories') == categories
