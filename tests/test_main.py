import importlib
import pytest

def test_main_prints_running(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Import the CLI module and call main().
    We only assert that 'running!' appears to keep this robust
    against small changes to your banner text.
    """
    from concordia_anthropology import main as cli

    importlib.reload(cli)

    cli.main()
    out = capsys.readouterr().out
    assert "running!" in out.lower()


def test_pydantic_round_trip() -> None:
    """
    A trivial Pydantic model to ensure pydantic>=2 is wired up.
    """
    from pydantic import BaseModel

    class Person(BaseModel):
        name: str
        age: int

    p = Person(name="Fred", age=42)
    assert p.model_dump() == {"name": "Fred", "age": 42}
