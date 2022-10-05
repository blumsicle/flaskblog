"""Test other random functions."""

from dotenv import load_dotenv
from smoothblog import create_app


def test_config():
    """
    GIVEN an uninitialized app
    WHEN the real app gets created
    THEN it should not be in testing mode
    """
    load_dotenv()
    assert not create_app().testing


def test_init_db_command(runner, monkeypatch):
    """
    GIVEN a command line
    WHEN the init-db command is run
    THEN it should initialze the database
    """

    class Recorder:
        """Ensure function was called"""

        called = False

    def fake_init_db():
        """Record function call"""
        Recorder.called = True

    monkeypatch.setattr("smoothblog.cli.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized the database" in result.output
    assert Recorder.called
