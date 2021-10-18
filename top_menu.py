from kivy_garden.contextmenu import AppMenu
from kivy.clock import mainthread
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionGroup
from kivy.app import App
from kivy_garden.contextmenu import ContextMenuTextItem
from kivy_garden.contextmenu import ContextMenu
from kivy_garden.contextmenu import AppMenuTextItem

import data_manager


class TopMenu(AppMenu):
    def populate_scripts(self):
        @mainthread
        def delayed():
            print(self.ids)

        delayed()

        app = App.get_running_app()
        scripts = data_manager.data_man.store.get("scripts", [])
        menu = [x for x in self.children if x.text.lower() == "scripts"][0]
        menu.clear_widgets()
        cm = ContextMenu()
        for script in scripts:

            def run(self, *args):
                lnd = data_manager.data_man.lnd
                exec(scripts[self.text])

            cm.add_widget(ContextMenuTextItem(text=script, on_release=run))
        menu.add_widget(cm)
        cm._on_visible(False)

    def add_console_menu(self, cbs):
        menu = [x for x in self.children if x.text.lower() == "view"][0]
        menu.clear_widgets()
        cm = ContextMenu()
        cm.add_widget(ContextMenuTextItem(text="Load", on_release=cbs.load))
        cm.add_widget(ContextMenuTextItem(text="Run", on_release=cbs.run))
        cm.add_widget(ContextMenuTextItem(text="Install", on_release=cbs.install))
        cm.add_widget(ContextMenuTextItem(text="Delete", on_release=cbs.delete))
        menu.add_widget(cm)
        cm._on_visible(False)