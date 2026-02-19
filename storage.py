import json
from pathlib import Path

EXCLUDED_FILE = Path("excluded_users.json")

def load_excluded() -> set[str]:
    if not EXCLUDED_FILE.exists():
        return set()
    try:
        content = EXCLUDED_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return set()
        data = json.loads(content)
    except json.JSONDecodeError:
        return set()
    if not isinstance(data, list):
        return set()
    return {x for x in data if isinstance(x, str)}

def save_excluded(excluded: set[str]) -> None:
    EXCLUDED_FILE.write_text(
        json.dumps(sorted(excluded), ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def toggle_user_excluded(user: str) -> set[str]:
    excluded = load_excluded()
    if user in excluded:
        excluded.remove(user)
    else:
        excluded.add(user)
    save_excluded(excluded)
    return excluded