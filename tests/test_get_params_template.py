import vcr

from tests import client


@vcr.use_cassette()
def test_retrieve_templates_by_non_existent_id():
    """Test endpoint templates passing an id"""
    match_template = client.get_templates(id=1_234)

    if match_template:
        assert isinstance(match_template, dict)
    else:
        assert match_template == []


@vcr.use_cassette()
def test_retrieve_templates_by_existent_id():
    """Test endpoint templates passing an id"""
    match_template = client.get_templates(id=4)
    if match_template:
        assert match_template.get('id') == 4
    else:
        assert match_template == []
