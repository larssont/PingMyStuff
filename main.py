import requests
import yaml
import argparse
from cerberus import Validator
from schema_config import schema

config_file = ""
conf_vars = {"name": None, "address": None, "status": None}
config = {}


def load_config():
    global config
    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


def write_config():
    with open(config_file, "w") as file:
        yaml.dump(config, file)


def validate_conf():
    v = Validator(schema)
    if not v.validate(config):
        raise Exception(v.errors)


def insert_conf_vars(text):
    new_text = text
    for key, value in conf_vars.items():
        old = f"{{{{ {key} }}}}"
        new_text = new_text.replace(old, str(value))
    return new_text


def get_args():
    global config_file
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="YAML config file path")
    args = parser.parse_args()
    config_file = args.config


def send_notification(notifier_val, status, site):
    data = dict.get(notifier_val, "data")
    if data is None:
        data = {}

            text = (
                config["message"]["up"] if status == 200 else config["message"]["down"]
            )

            conf_vars["name"] = site
            conf_vars["address"] = config["sites"][site]["address"]
            conf_vars["status"] = status

            text = insert_conf_vars(text)

            data[v["messageDataName"]] = text
            address = v["address"]
            requests.post(address, data=data)


def get_status(address):
    return requests.get(address).status_code


def insert_conf_vars(text):
    new_text = text
    for key, value in conf_vars.items():
        old = f"{{{{ {key} }}}}"
        new_text = new_text.replace(old, str(value))
    return new_text


def run():
    for k, v in config["sites"].items():
        address = v["address"]
        old_status = config["sites"][k].get("status")
        new_status = get_status(address)

        if old_status != new_status:
            notify(k, new_status)
            config["sites"][k]["status"] = new_status
            write_config()


def main():
    get_args()
    load_config()
    validate_conf()
    run()


if __name__ == "__main__":
    main()
