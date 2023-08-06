from datetime import date
from pathlib import Path
import orjson
import requests

from . import models

# functions to update local and remote data


def get_local_config() -> models.Settings:
    """Get the config.json file from the project's root."""
    return models.Settings()  # type: ignore


def get_remote_config() -> models.Settings:
    """Get the config.json file from the project's root on GitHub."""
    url = (
        "https://raw.githubusercontent.com/UK-IPOP/open-data-pipeline/main/config.json"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError(resp.content)
    return models.Settings.parse_raw(resp.content)


def update_local_config(config: models.Settings):
    """Update the local config.json file."""
    json_data = config.json(indent=2)
    with open(Path("config.json"), "w") as f:
        f.write(json_data)


def update_remote_config(config: models.Settings):
    """Update the remote config.json file."""
    if config.github_token is None:
        raise ValueError("github_token is required to update remote config")
    url = (
        "https://raw.githubusercontent.com/UK-IPOP/open-data-pipeline/main/config.json"
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {config.github_token}",
    }
    data = {}
    today = date.today().strftime("%Y-%m-%d")
    data["message"] = f"Update config.json ({today})"
    data["content"] = config.json(indent=2)

    resp = requests.put(url, headers=headers, data=orjson.dumps(data))
    if resp.status_code != 200:
        raise ValueError(resp.content)
