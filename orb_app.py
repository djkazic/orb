from kivy.app import App
from main_layout import MainLayout
import data_manager
import json
from kivy.lang import Builder
from pathlib import Path


class OrbApp(App):
    title = "Lightning orb"

    def load_kvs(self):
        for path in [str(x) for x in Path(".").rglob("*.kv")]:
            if path != "orb.kv" and "tutes" not in path:
                Builder.load_file(path)

    def build(self):
        self.load_kvs()
        data_manager.data_man = data_manager.DataManager(config=self.config)
        main_layout = MainLayout()
        return main_layout

    def build_config(self, config):
        config.add_section("lnd")
        config.set("lnd", "hostname", "localhost:10009")
        config.set("lnd", "lnd_dir", "~/.lnd")
        config.set("lnd", "network", "mainnet")

    def build_settings(self, settings):
        settings.add_json_panel(
            "Orb",
            self.config,
            data=json.dumps(
                [
                    {"type": "title", "title": "Connection Settings"},
                    {
                        "type": "string",
                        "title": "Host",
                        "desc": "The node's FQDN:PORT, e.g localhost:10009",
                        "section": "lnd",
                        "key": "hostname",
                    },
                    {
                        "type": "string",
                        "title": "lnd dir",
                        "desc": "Path to .lnd directory",
                        "section": "lnd",
                        "key": "lnd_dir",
                    },
                    {
                        "type": "options",
                        "title": "Network",
                        "desc": "Network to connect to",
                        "section": "lnd",
                        "key": "network",
                        "options": ["mainnet", "testnet"],
                    },
                ]
            ),
        )

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
        data_manager.data_man = data_manager.DataManager(config=self.config)
