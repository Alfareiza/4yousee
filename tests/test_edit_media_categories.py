from tests import client


def test_edit_category_name():
    """Test endpoint put and passing the name"""
    name = 'Sample name via API'
    response = client.edit_category(id=6, name=name)
    assert response.get('name') == name


def test_edit_category_description():
    """Test endpoint put and passing only the description"""
    description = 'Sample description from API'
    response = client.edit_category(id=6, description=description)
    assert response.get('description') == description


def test_edit_category_parent():
    """Test endpoint put and passing only the parent"""
    response = client.edit_category(id=6, parent=2)
    assert response.get('parent')['id'] == 2
