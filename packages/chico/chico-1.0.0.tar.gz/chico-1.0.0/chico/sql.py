#!/usr/bin/env python3
import urllib.parse
from sqlalchemy import create_engine, engine_from_config
from sqlalchemy.engine import make_url, URL


class DB:
    def __init__(
        self,
        username=None,
        password=None,
        host=None,
        database=None,
        port=None,
        dialect="mysql",
        driver="pymysql",
        **query,
    ):
        self.config = {
            "username": username,
            "password": self._parse_passwd(password),
            "host": host,
            "port": port,
            "database": database,
            "driver": driver,
            "dialect": dialect,
            "query": query,
        }
        self.url = make_url(self._str_url(self.config))

    @staticmethod
    def _str_url(config):
        "dialect[+driver]://user:password@host/dbname[?key=value..]"
        return URL.create(
            drivername=config["dialect"]
            if config["driver"] is None
            else f"{config['dialect']}+{config['driver']}",
            username=config["username"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=config["database"],
            query=config["query"],
        )

    @staticmethod
    def _parse_passwd(password):
        return urllib.parse.quote_plus(password)
