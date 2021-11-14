from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivymd.uix.datatables import MDDataTable

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc.ui_actions import console_output


class RankingsFileChooser(PopupDropShadow):

    selected_path = StringProperty('')


class RankingsExportPath(PopupDropShadow):

    selected_path = StringProperty('')


class Rankings(PopupDropShadow):
    @guarded
    def __init__(self, *args):
        super(Rankings, self).__init__(*args)

        self.checked_pks = set([])

    def open(self, *args):
        super(Rankings, self).open(*args)
        from orb.store.node_rank import count_successes_failures

        self.pks, row_data = count_successes_failures()

        if row_data:
            self.data_tables = MDDataTable(
                use_pagination=True,
                rows_num=25,
                check=True,
                column_data=[
                    ("Alias", dp(60)),
                    ("Successes", dp(30), self.sort_on_signal),
                    ("Failures", dp(30)),
                ],
                row_data=row_data,
                sorted_on="Successes",
                sorted_order="ASC",
                elevation=2,
            )
            self.ids.box_layout.add_widget(self.data_tables)
            self.data_tables.bind(on_check_press=self.on_check_press)
        else:
            self.ids.box_layout.add_widget(
                Label(
                    text=(
                        'This feature ranks nodes by how predictable\n'
                        'they are at routing payments.\n'
                        'No path-finding data available.\n'
                        'Make payments, or circular rebalances.'
                    )
                )
            )

    @guarded
    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))

    @guarded
    def ingest(self):
        dialog = RankingsFileChooser()
        dialog.open()

        def do_ingest(widget, path):
            from orb.store import node_rank

            node_rank.ingest(path)

        dialog.bind(selected_path=do_ingest)

    @guarded
    def export(self):
        dialog = RankingsExportPath()
        dialog.open()

        def do_export(widget, path):
            from orb.store import node_rank

            node_rank.export(path)

        dialog.bind(selected_path=do_export)

    def copy_pks(self):
        Clipboard.copy('\n'.join(self.checked_pks))
        console_output(f'Copied {len(self.checked_pks)} pubkeys to clipboard')

    def on_check_press(self, _, row_data):
        pk = self.pks[row_data[0]]
        if pk in self.checked_pks:
            self.checked_pks.remove(pk)
        else:
            self.checked_pks.add(pk)
