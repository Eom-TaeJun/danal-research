import json
from pathlib import Path

CONTEXT_DIR = "outputs/context"


def load_latest(pattern: str) -> dict:
    """outputs/context/에서 가장 최신 파일 로드"""
    files = sorted(Path(CONTEXT_DIR).glob(pattern), reverse=True)
    if not files:
        return {}
    with open(files[0], encoding="utf-8") as f:
        return json.load(f)
