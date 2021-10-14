from functools import lru_cache
import base64, codecs, json, requests
from kivy.app import App
import os
from munch import Munch


class Lnd:
    def __init__(self):
        app = App.get_running_app()
        data_dir = app.user_data_dir
        self.cert_path = os.path.join(data_dir, "tls.cert")
        self.hostname = app.config["lnd"]["hostname"]
        self.rest_port = app.config["lnd"]["rest_port"]
        macaroon = app.config["lnd"]["macaroon_admin"]
        self.headers = {"Grpc-Metadata-macaroon": macaroon.encode()}

    @property
    def fqdn(self):
        return f"https://{self.hostname}:{self.rest_port}"

    def get_balance(self):
        url = f"{self.fqdn}/v1/balance/blockchain"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def channel_balance(self):
        url = f"{self.fqdn}/v1/balance/channels"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def get_channels(self, active_only=False):
        url = f"{self.fqdn}/v1/channels"
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data={"active_only": active_only},
        )
        return Munch.fromDict(r.json()).channels

    @lru_cache(maxsize=None)
    def get_info(self):
        url = f"{self.fqdn}/v1/getinfo"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    @lru_cache(maxsize=None)
    def get_edge(self, channel_id):
        url = f"{self.fqdn}/v1/graph/edge/{channel_id}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def get_policy_to(self, channel_id):
        edge = self.get_edge(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return Munch.fromDict(edge.node1_policy)
        return Munch.fromDict(edge.node2_policy)

    def get_policy_from(self, channel_id):
        edge = self.get_edge(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return Munch.fromDict(edge.node2_policy)
        return Munch.fromDict(edge.node1_policy)

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    @lru_cache(maxsize=None)
    def get_node_alias(self, pub_key):
        url = f"{self.fqdn}/v1/graph/node/{pub_key}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json()).node.alias

    def fee_report(self):
        url = f"{self.fqdn}/v1/fees"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

if __name__ == "__name__":
    lnd = Lnd()
    lnd.get_balance()