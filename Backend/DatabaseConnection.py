import os
from pathlib import Path

import mysql.connector


class DatabaseConnection:
    """Creates MySQL connections from environment variables."""

    def __init__(self, env_path=".env"):
        self._base_dir = Path(__file__).resolve().parent
        self._load_env(self._base_dir / env_path)

    def connect(self):
        ssl_ca = os.getenv("MYSQL_SSL_CA")
        if ssl_ca and not Path(ssl_ca).is_absolute():
            ssl_ca = str(self._base_dir / ssl_ca)

        config = {
            "host": self._required_env("MYSQL_HOST"),
            "port": int(os.getenv("MYSQL_PORT", "3306")),
            "user": self._required_env("MYSQL_USER"),
            "password": self._required_env("MYSQL_PASSWORD"),
            "database": self._required_env("MYSQL_DATABASE"),
        }

        if ssl_ca:
            config["ssl_ca"] = ssl_ca

        return mysql.connector.connect(**config)

    def _required_env(self, name):
        value = os.getenv(name)
        if not value:
            raise RuntimeError(f"Environment variable {name} is required")
        return value

    def _load_env(self, path):
        if not path.exists():
            return

        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
