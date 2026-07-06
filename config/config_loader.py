from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


def _resolve_config_path() -> Path:
    config_file = os.getenv("CONFIG_FILE")
    if not config_file:
        return DEFAULT_CONFIG_PATH

    path = Path(config_file)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def load_config() -> dict[str, Any]:
    config_path = _resolve_config_path()
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_environment() -> str:
    return os.getenv("API_ENV", "demo")


def get_config() -> dict[str, Any]:
    environment = get_environment()
    config = load_config()

    if environment not in config:
        available = ", ".join(config.keys())
        raise KeyError(f"Environment '{environment}' not found. Available environments: {available}")

    return config[environment]


def get_base_url() -> str:
    return get_config()["base_url"]


def get_timeout() -> int:
    return int(get_config().get("timeout", 10))


def get_default_headers() -> dict[str, str]:
    return dict(get_config().get("headers", {}))


def get_auth_credentials() -> tuple[str, str]:
    auth_config = get_config().get("auth", {})
    return auth_config["username"], auth_config["password"]


def get_max_response_time_ms() -> int:
    performance_config = get_config().get("performance", {})
    return int(performance_config.get("max_response_time_ms", 3000))
