from pathlib import Path
import shutil


def setup():
    p = Path("data")
    if p.exists():
        shutil.rmtree(p)
    p.mkdir()


def teardown():
    p = Path("data")
    shutil.rmtree(p)
    Path("extracted_drugs.jsonl").unlink()
