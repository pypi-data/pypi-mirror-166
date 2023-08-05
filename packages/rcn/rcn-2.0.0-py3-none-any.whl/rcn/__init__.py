# import argparse
#
#
# from rcn.utils import configDir
#
# from yaml import SafeLoader, load, dump, SafeDumper
# import os
# from getpass import getpass
# import rcn.profile_func
#
# def profile(actions):
#     if actions[0] == "ls":
#         rcn.profile_func.ls()
#     elif actions[0] == "set-default":
#         rcn.profile_func.setDefault(actions[1])
#     elif actions[0] == "configure":
#         rcn.profile_func.configure(actions[1])
#     elif actions[0] == "delete":
#         rcn.profile_func.delete(actions[1])
#
# def configure(profile, server_url=""):
#     import requests
#     x = input(f"Server Url({server_url}): ")
#     if x.strip() != "":
#         server_url = x
#
#     client_id = input("Client Id: ")
#     username = input("Username: ")
#     password = getpass()
#
#
#     response = requests.post(f"{server_url}/openid-connect/token", data={
#         'username': username,
#         'password': password,
#         'client_id': client_id,
#         'grant_type': 'password'
#     })
#
#     data = {
#         "server": server_url,
#         "profile": profile,
#         "data": response.json()
#     }
#     absPath = os.path.join(configDir, f"{profile}.yml")
#     with open(absPath, "w") as file:
#         dump(data, file)