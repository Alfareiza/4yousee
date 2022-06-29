import pytest

from tests import client


@pytest.mark.parametrize('upload_id', ['123', '5021b3b7c402468d5b018a8b4a2b448a'])
def test_retrieve_upload_by_id(upload_id):
    """Test endpoint uploads passing an id"""
    match_upload = client.get_uploads(id='upload_id')
    if match_upload:
        assert isinstance(match_upload, dict)
        assert len(match_upload.keys()) == 2
        assert match_upload.get('id')
        assert match_upload.get('filename')
    else:
        assert match_upload == []
