import argparse
import base64

from requests import post

from rcn.utils import configDir
from yaml import dump, load, SafeLoader
import os, json

prompts = dict(client_id=dict(defaultValue="", prompt="Client Id"),
               username=dict(defaultValue="", prompt="Username"),
               server=dict(defaultValue="", prompt="Server Url"))


def configure(profile):
    absPath = os.path.join(configDir, f"{profile}.yml")
    if os.path.exists(absPath):
        with open(absPath, "r") as stream:
            data = stream.read()
            config_data = load(data, Loader=SafeLoader)
            for (key, value) in prompts.items():
                if key in config_data:
                    value['defaultValue'] = config_data.get(key)

    data = dict()
    for key, value in prompts.items():
        tempValue = input(f"{value.get('prompt')} [{value.get('defaultValue')}]: ")
        if tempValue.strip() == "":
            data[key] = value.get('defaultValue')
        else:
            data[key] = tempValue

    password = input("Password: ")
    server_url = data.get('server')

    response = post(f"{server_url}/openid-connect/token", data={
        'username': data.get('username'),
        'client_id': data.get('client_id'),
        'password': password,
        'grant_type': 'password'
    })

    credentials = base64.b64encode(json.dumps(response.json()).encode()).decode()
    data = {
        **data,
        "profile": profile,
        "data": credentials
    }

    with open(absPath, "w") as file:
        dump(data, file)


def login(profile):
    absPath = os.path.abspath(os.path.join(configDir, f"{profile}.yml"))
    with open(absPath, "r") as stream:
        data = stream.read()
        config_data = load(data, Loader=SafeLoader)

    server_url = config_data.get('server')
    client_id = config_data.get('client_id')

    credentials = base64.b64decode(config_data.get('data').encode()).decode()
    refresh_token = json.loads(credentials).get('refresh_token')

    response = post(f"{server_url}/openid-connect/token", data={
        'client_id': client_id,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    })

    credentials = base64.b64encode(json.dumps(response.json()).encode()).decode()
    data = {
        **config_data,
        "data": credentials
    }

    absPath = os.path.join(configDir, f"{profile}.yml")
    with open(absPath, "w") as file:
        dump(data, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("actions", nargs='*', type=str)
    parser.add_argument("--profile", default="default", help="configure a specific profile. Default - default")
    namespace = parser.parse_args()
    profile_name = namespace.profile
    actions = namespace.actions

    if actions[0].strip() == "configure":
        configure(profile_name)
    if actions[0].strip() == "login":
        login(profile_name)
