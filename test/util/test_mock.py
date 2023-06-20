from src.util.mock import mock


def test_mock_message():
    assert mock("Some Message") == "SoMe MeSsAgE"
    assert mock("Space     Message") == "SpAcE     mEsSaGe"
    assert mock("") == ""
    assert mock("     ") == "     "
