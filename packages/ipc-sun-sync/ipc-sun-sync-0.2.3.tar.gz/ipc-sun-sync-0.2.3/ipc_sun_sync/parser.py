import argparse
from datetime import timedelta
import pathlib
import sys
import logging
from typing import Dict

import astral
import pytz
import yaml
import pytimeparse

from .constants import Config, ConfigMethod, ConfigIPC
from . import __description__


def parse_args():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="enable verbose logging",
    )
    parser.add_argument(
        "--check", action="store_true", dest="check", help="check configuration"
    )
    parser.add_argument(
        "--verify", action="store_true", dest="verify", help="verify ipc settings"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=pathlib.Path,
        metavar="PATH",
        dest="path",
        required="-V" not in sys.argv
        and "--version" not in sys.argv
        and "-T" not in sys.argv
        and "--timezones" not in sys.argv,
        help="configuration file path",
    )
    parser.add_argument(
        "-V",
        "--version",
        dest="version",
        action="store_true",
        help="show version",
    )
    parser.add_argument(
        "-T",
        "--timezones",
        dest="timezones",
        action="store_true",
        help="show all timezones",
    )
    return parser.parse_args()


def parse_yml_or_exit(path: pathlib.Path):
    try:
        with path.open(mode="r") as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        logging.error("file '%s' does not exist", path)
    except PermissionError:
        logging.error("file '%s' is not readable", path)
    except yaml.YAMLError as error:
        logging.error(error)
    exit(1)


def parse_method_or_exit(method: str) -> ConfigMethod:
    if method == "cgi":
        return ConfigMethod.CGI
    if method == "rpc":
        return ConfigMethod.RPC
    logging.error("method '%s' invalid", method)
    exit(1)


def parse_offset(offset: str) -> timedelta:
    return timedelta(seconds=pytimeparse.parse(offset))


def parse_config_or_exit(yml: Dict) -> Config:
    timezone = str(yml["timezone"])
    if timezone not in pytz.all_timezones:
        logging.error("timezone '%s' is invalid", timezone)
        exit(1)

    username = str(yml["username"]) if "username" in yml else "admin"
    password = str(yml["password"])
    method = (
        parse_method_or_exit(str(yml["method"]))
        if "method" in yml
        else ConfigMethod.CGI
    )
    sunrise_offset = (
        parse_offset(str(yml["sunrise_offset"]))
        if "sunrise_offset" in yml
        else timedelta()
    )
    sunset_offset = (
        parse_offset(str(yml["sunset_offset"]))
        if "sunset_offset" in yml
        else timedelta()
    )

    config: Config = {
        "location": astral.LocationInfo(
            name="custom",
            region="custom",
            timezone=timezone,
            latitude=float(yml["latitude"]),
            longitude=float(yml["longitude"]),
        ),
        "ipc": [],
    }

    for c in yml["ipc"]:
        ip = str(c["ip"])
        ipc_config: ConfigIPC = {
            "ip": ip,
            "name": str(c["name"]) if "name" in c else ip,
            "username": str(c["username"]) if "username" in c else username,
            "password": str(c["password"]) if "password" in c else password,
            "channel": int(c["channel"]) if "channel" in c else 0,
            "method": parse_method_or_exit(str(c["method"]))
            if "method" in c
            else method,
            "sunrise_offset": parse_offset(str(c["sunrise_offset"]))
            if "sunrise_offset" in c
            else sunrise_offset,
            "sunset_offset": parse_offset(str(c["sunset_offset"]))
            if "sunset_offset" in c
            else sunset_offset,
        }

        config["ipc"].append(ipc_config)

    return config
