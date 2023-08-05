import requests
import os

from cndi.env import getContextEnvironment, loadEnvFromFile

from rcn.utils import loadyaml, configDir

class RCNZmqFlowHttpClient:
    """
    RCNZmqFlowHttpClient: Client to configure the zmq processor server while using the Video Streaming in RCN
    """
    def __init__(self):
        self.hostUrl = getContextEnvironment("rcn.hosts.zmq.url", defaultValue=None)

    def listConnectors(self):
        response = requests.get(f"{self.hostUrl}/getConnectors")
        return response.json()

class RCNVideoServerClient:
    """
    RCNVideoServer Client: Client to configure the Video Signaling Server for WebRTC
    """
    def __init__(self):
        self.__token = None
        self.hostUrl = getContextEnvironment("rcn.hosts.media.url", defaultValue=None)
        self.subscriptionKeyEnabled = getContextEnvironment("rcn.client.security.enabled", defaultValue=False, castFunc=bool)
        self.subscriptionKey = getContextEnvironment("rcn.client.security.apiKey", defaultValue=None)
        if not self.subscriptionKeyEnabled:
            raise ValueError(f"RCN Security disabled, security needs to be enabled from configuration rcn.client.security.enabled=True")
        elif self.subscriptionKey is None:
            raise NotImplementedError(f"Subscription Key cannot be null when rcn security is enabled")

        assert self.hostUrl is not None, "Media Server url cannot be null, check for rcn.hosts.media.url"

    def videoFilter(self, connectorName, action: str):
        url = f"{self.hostUrl}/api/pipeline/element?connectorName={connectorName}"
        if action.upper() == "ADD":
             response = requests.post(url, headers={
                    "subscriptionKey": self.subscriptionKey
                })
        elif action.upper() == "DELETE":
            response = requests.delete(url, headers={
                    "subscriptionKey": self.subscriptionKey
                })

        return response.json(), response.status_code

class RCNBaseHttpClient:
    def __init__(self):
        self.subscriptionKeyEnabled = getContextEnvironment("rcn.client.security.enabled", defaultValue=False, castFunc=bool)
        self.subscriptionKey = getContextEnvironment("rcn.client.security.apiKey", defaultValue=None)
        if not self.subscriptionKeyEnabled:
            raise ValueError(f"RCN Security disabled, security needs to be enabled from configuration rcn.client.security.enabled=True")
        elif self.subscriptionKey is None:
            raise NotImplementedError(f"Subscription Key cannot be null when rcn security is enabled")


    def get(self, url, params={}):
        return requests.get(url, params=params, headers={
            "subscriptionKey": self.subscriptionKey
        })

    def post(self, url, params={}, body={}):
        return requests.post(url, params=params, json=body, headers={
            "subscriptionKey": self.subscriptionKey
        })

class RCNBackendServerClient(RCNBaseHttpClient):
    def __init__(self):
        RCNBaseHttpClient.__init__(self)
        self.serverUrl = getContextEnvironment("rcn.hosts.tunnel.url")

    def issueVideoSession(self):
        response = self.post(f"{self.serverUrl}/videosession", body={

        })

class RCNTunnelServerClient(RCNBaseHttpClient):
    """
    RCNTunnelServerClient: Client to configure the RCN Tunnel Client
    """
    def __init__(self):
        RCNBaseHttpClient.__init__(self)
        self.hostUrl = getContextEnvironment("rcn.hosts.tunnel.url", defaultValue=None)
        assert self.hostUrl is not None, "Tunnel Server url cannot be null, check for rcn.hosts.tunnel.url"

    def checkForAvailableDevice(self, deviceCode):
        url = f"{self.hostUrl}/api/connections/device/available?deviceCode={deviceCode}"
        response = self.get(url)

        if response.status_code == 200:
            return response.content.decode().lower() == "true", response.status_code

        return False, response.status_code

    def forwardMessage(self, deviceCode, socketMessage):
        url = f"{self.hostUrl}/api/drone/"

class RCNHttpClient:
    def __init__(self, **kwargs):
        self.config = {
            "server": "http://localhost:8080/backend",
            **kwargs
        }
        if os.path.exists(os.path.join(configDir, "default.yml")):
            self.loadToken()

    def loadToken(self, profile='default'):
        rcnConfig = loadyaml(os.path.join(configDir, f"{profile}.yml"))
        self.setToken(rcnConfig['token'])

    def setToken(self, token):
        self.__token = token

    def login(self, credentials):
        response = requests.post(f"{self.config['server']}/login", json={
            "username": credentials['username'],
            "password": credentials['password']
        })
        responseData = response.json()
        if response.status_code == 200 and "jwt" in responseData:
            self.setToken(responseData['jwt'])

        return response

    def getDevices(self):
        response = requests.get(f"{self.config['server']}/auth/device/list", headers={
            "Authorization": f"Bearer {self.__token}"
        })

        return response.json()

    def getSingleDevice(self, id):
        response = requests.get(f"{self.config['server']}/auth/device/?id={id}", headers={
            "Authorization": f"Bearer {self.__token}"
        })
        return response.json()

    def getConfigJson(self, connectionId, deviceId):
        response = requests.get(f"{self.config['server']}/connections/getConfiguration?id={connectionId}&deviceId={deviceId}", headers={
            "Authorization": f"Bearer {self.__token}"
        })
        return response.text

    def getSupportedDevices(self):
        response = requests.get(f"{self.config['server']}/public/api/supported")
        return response.json()


    def getConnections(self):
        response = requests.get(f"{self.config['server']}/connections/list", headers={
            "Authorization": f"Bearer {self.__token}"
        })

        return response.json()