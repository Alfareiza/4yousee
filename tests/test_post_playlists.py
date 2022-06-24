from tests import client


def test_post_playlists():
    """Test endpoint post and passing the required fields"""
    name = 'sample playlist'
    items = [{'type': 'media', 'id': 39, 'name': 'Hombre_Reloj_Admobilize',
              'file': 'i_39.mp4', 'durationInSeconds': 6,
              'categories': [{'id': 1, 'name': 'DEMO'}],
              'contentSchedule': {'startDate': '2050-11-26'}},
             {'type': 'media', 'id': 40, 'name': 'Sin_Genero_Viajes_Admobilize',
              'file': 'i_40.mp4', 'durationInSeconds': 6,
              'categories': [{'id': 1, 'name': 'DEMO'}],
              'contentSchedule': {'startDate': '2050-11-26'}}]
    sequence = [0, 1]
    response = client.post_playlists(name=name, items=items, sequence=sequence)
    assert response.get('name') == name
    assert response.get('items') == items
    assert response.get('sequence') == sequence
    client.delete_playlist(response.get('id'))
