import pytest
import vcr

from tests import client


@vcr.use_cassette()
def test_retrieve_reports_by_non_existent_id():
    """Test endpoint reports passing an id"""
    with pytest.raises(Exception):
        client.get_reports(123_4567_890)


@vcr.use_cassette()
def test_retrieve_reports_by_existent_id():
    """Test endpoint reports passing an non existent id"""
    report_input = 521585
    match_report = client.get_reports(id=report_input)
    assert isinstance(match_report, dict)
    assert match_report.get('id') == report_input


@vcr.use_cassette()
def test_retrieve_reports_not_belong_to_user():
    """Test endpoint reports passing an id that
    does not belong to the user"""
    with pytest.raises(Exception, match='{"message":"Report with'
                                        ' ID 158542 does not belong '
                                        'to current user"}'):
        client.get_reports(id=158542)
