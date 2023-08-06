import os


def get_env_extra() -> dict[str, str]:
    res = {
        "progname": "LOGTMP-PROGNAME",
        "request_id": "LOGTMP-X-REQUEST-ID",
    }
    env_extra_str = os.environ.get("LOG_ENV_EXTRA")
    if env_extra_str:
        extra_list = env_extra_str.split(",")
        for extra in extra_list:
            key, val = extra.split(":")
            res[key.strip()] = val.strip()
    return res


def get_extra_from_environ() -> dict[str, str]:
    return {key: value for key, ename in get_env_extra().items() if (value := os.environ.get(ename))}


def set_extra_to_environ(key: str, value: str) -> None:
    os.environ[get_env_extra().get(key, key)] = value
