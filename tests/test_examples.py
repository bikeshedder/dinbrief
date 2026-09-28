import runpy
from pathlib import Path

EXAMPLES = Path(__file__).parent.parent / "examples"


def test_invoice_example(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(EXAMPLES / "invoice.py"), run_name="__main__")
    assert (tmp_path / "invoice.pdf").read_bytes().startswith(b"%PDF-")
