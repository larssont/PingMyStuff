import requests
import yaml

config_path = r"./config.yml"
config = {}

conf_vars = {"name": None, "address": None, "status": None}


def load_config():
    global config
    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


def write_config():
    with open(config_path, "w") as file:
        yaml.dump(config, file)


def notify(site, status):
    for notifier in config["notifiers"]:
        v = next(iter(notifier.values()))
        sites = v["sites"]

        if site in sites:
            data = dict.get(v, "data")
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


if __name__ == "__main__":
    load_config()
    run()
