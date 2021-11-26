import math
from collections import defaultdict
from functools import cmp_to_key

import bezier
from colour import Color as Colour

from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics import Mesh
from kivy.graphics.tesselator import Tesselator

from orb.misc.Vector import Vector
from orb.misc.lerp import lerp_vec
import data_manager


class ChordWidget(Widget):
    def __init__(self, channels, *args, **kwargs):
        super(ChordWidget, self).__init__(*args, **kwargs)

        self.channels = channels
        self.radius = 950

        matrix = self.get_matrix()
        # from random import shuffle, randrange

        # r = [*(range(19))]
        # shuffle(r)
        # matrix = {}
        # for i in r:
        #     matrix[(10, i)] = randrange(1000, 5000)

        with self.canvas:
            offset = 0
            sec_w = 360 / len(channels)
            sec_w2 = 360 / len(channels) / 2.5
            cols = [*Colour("red").range_to("blue", len(channels))]
            chan_pos = {}
            chan_cols = {}
            for chan, col in zip(channels, cols):
                Color(rgb=col.rgb)
                chan_cols[chan.chan_id] = col.rgb
                self.chord = Line(
                    circle=(0, 0, self.radius, offset - sec_w2, offset + sec_w2),
                    width=5,
                    cap="none",
                )
                chan_pos[chan.chan_id] = offset
                offset += sec_w

            for chan, col in zip(channels, cols):
                show = data_manager.data_man.store.get("show_to_chords", {}).get(
                    str(chan.chan_id), False
                )
                if show:
                    c = col.rgb
                    Color(rgba=(c[0], c[1], c[2], 0.5))
                    self.draw_channel_chords(
                        chan.chan_id,
                        col,
                        chan_pos,
                        matrix,
                        offset,
                        sec_w,
                        sec_w2,
                        chan_cols,
                    )

    def draw_channel_chords(
        self, out_chan, col, chan_pos, matrix, offset, sec_w, sec_w2, chan_cols
    ):
        def offset_to_pos(offset):
            x = math.sin(offset / 360 * 3.14378 * 2) * self.radius
            y = math.cos(offset / 360 * 3.14378 * 2) * self.radius
            return (x, y)

        in_chans = [x[1] for x in matrix if x[0] == out_chan and x[1] in chan_pos]

        def sort_by_pos(a, b):
            a = (chan_pos[a] - chan_pos[out_chan]) % 360
            b = (chan_pos[b] - chan_pos[out_chan]) % 360
            if a == b:
                return 0
            if a < b:
                return 1
            else:
                return -1

        in_chans.sort(key=cmp_to_key(sort_by_pos))

        def get_line_points(out_chan_deg, in_chan_deg, inverted=False):
            x, y = offset_to_pos(out_chan_deg)
            x1, y1 = offset_to_pos(in_chan_deg)
            a, b = Vector(x, y), Vector(x1, y1)
            dot = a.normalized().dot(b.normalized())
            b_mid_x, b_mid_y = lerp_vec(Vector(0, 0), a.mid(b), max(0, dot))
            curve1 = bezier.Curve(
                [
                    [x, b_mid_x, x1],
                    [y, b_mid_y, y1],
                ],
                degree=2,
            )
            points = []
            step = 100
            for f in range(step):
                e = curve1.evaluate(f / step)
                points.extend([float(e[int(inverted)]), float(e[int(not inverted)])])
            return points if not inverted else points[::-1]

        total_liq = sum(matrix[(out_chan, in_chan)] for in_chan in in_chans)

        local_offset = offset - sec_w2
        dist = (offset + sec_w2) - local_offset
        for in_chan in in_chans:
            liq = matrix[(out_chan, in_chan)] / total_liq
            out_chan_deg, in_chan_deg = chan_pos[out_chan], chan_pos[in_chan]
            tess = Tesselator()
            points1 = get_line_points(
                out_chan_deg + local_offset, in_chan_deg + (liq * sec_w / 2.5)
            )
            local_offset += liq * dist
            points2 = get_line_points(
                out_chan_deg + local_offset,
                in_chan_deg - (liq * sec_w / 2.5),
                inverted=True,
            )
            tess.add_contour(points1 + points2)
            if tess.tesselate():
                c = chan_cols[in_chan]
                Color(rgba=(c[0], c[1], c[2], 0.5))
                for vertices, indices in tess.meshes:
                    Mesh(vertices=vertices, indices=indices, mode="triangle_fan")

    def get_matrix(self):
        matrix = defaultdict(int)
        from orb.store import model

        chan_ids = [c.chan_id for c in self.channels]
        for c in self.channels:
            hist = (
                model.FowardEvent()
                .select()
                .where(model.FowardEvent.chan_id_out == c.chan_id)
            )
            for h in hist:
                matrix[(h.chan_id_out, h.chan_id_in)] += h.amt_out

        return matrix

    def print_matrix(self, chan_ids, matrix):
        for ci in chan_ids:
            for cj in chan_ids:
                if ci != cj:
                    print(f"{matrix[(ci, cj)]:<10}", end="")
            print("")
