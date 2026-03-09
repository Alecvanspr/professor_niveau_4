import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def load_level_constraints() -> dict:
    config_path = Path(__file__).resolve().parent.parent / 'config' / 'level_constraints.json'
    with config_path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def get_level_constraints(level: int, framework_name: str | None = None) -> dict[str, list[str]]:
    data = load_level_constraints()
    framework_key = framework_name or 'default'

    framework_bucket = data.get(framework_key, data.get('default', {}))
    level_bucket = framework_bucket.get(str(level), {})

    return {
        'must_have': level_bucket.get('must_have', []),
        'must_not_have': level_bucket.get('must_not_have', []),
    }
