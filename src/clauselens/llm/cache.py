import hashlib
import json
from pathlib import Path


class ResponseCache:

    def __init__(self, cache_dir):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def make_key(self, model, prompt, system_instruction=None):

        request_data = {
            "model": model,
            "prompt": prompt,
            "system_instruction": system_instruction,
        }

        request_string = json.dumps(request_data, sort_keys=True)

        return hashlib.sha256(
            request_string.encode("utf-8")
        ).hexdigest()

    def get(self, key):

        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        with open(cache_file, "r") as file:
            return json.load(file)

    def put(self, key, data):

        cache_file = self.cache_dir / f"{key}.json"

        with open(cache_file, "w") as file:
            json.dump(data, file, indent=4)