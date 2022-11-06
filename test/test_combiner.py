from unittest.mock import MagicMock, patch
from .. import pdf_download_combine


@patch(pdf_download_combine.__name__+".logging.info")
def test_combiner(mock_log):
    
    file_name = pdf_download_combine.combine_pdfs(MagicMock(), "/asdf/other/")
    assert mock_log.call_count == 1


def test_downloader():
    """
    TODO: Write test
    """
    assert True


def test_processor():
    """
    TODO: Write test
    """
    assert True
