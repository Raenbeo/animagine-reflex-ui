import reflex as rx

from typing import NamedTuple
from enum import Enum


class Resolutions(NamedTuple):
    width: int
    height: int
    width_ratio: int
    height_ratio: int


class ResPreset(Enum):
    squre = Resolutions(1024, 1024, 1, 1)

    landscape1 = Resolutions(1152, 896, 9, 7)
    landscape2 = Resolutions(1216, 832, 3, 2)
    landscape3 = Resolutions(1344, 768, 7, 4)
    landscape4 = Resolutions(1536, 640, 12, 5)

    portrait1 = Resolutions(896, 1152, 7, 9)
    portrait2 = Resolutions(832, 1216, 2, 3)
    portrait3 = Resolutions(768, 1344, 4, 7)
    portrait4 = Resolutions(640, 1536, 5, 12)


class ResState(rx.State):
    width = ResPreset.portrait2.value.width
    height = ResPreset.portrait2.value.height
    ratio = f"{ResPreset.portrait2.value.width_ratio}:{ResPreset.portrait2.value.height_ratio}"

    @rx.event
    def set_width(self, v):
        if v == "":
            self.width = 0
        else:
            self.width = int(v)

    @rx.event
    def set_height(self, v):
        if v == "":
            self.height = 0
        else:
            self.height = int(v)

    @rx.event
    def set_preset(self, preset):
        self.width = preset[0]
        self.height = preset[1]
        self.ratio = f"{preset[2]}:{preset[3]}"


def resolution_ui() -> rx.Component:
    ui = rx.box(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.heading("Resolution"),
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.button("Choose Recommend Resolutions"),
                        ),
                        rx.dialog.content(
                            rx.grid(
                                preset_button("LandScape", ResPreset.landscape1),
                                preset_button("LandScape", ResPreset.landscape2),
                                preset_button("LandScape", ResPreset.landscape3),
                                preset_button("LandScape", ResPreset.landscape4),
                                preset_button("Portrait", ResPreset.portrait1),
                                preset_button("Portrait", ResPreset.portrait2),
                                preset_button("Portrait", ResPreset.portrait3),
                                preset_button("Portrait", ResPreset.portrait4),
                                preset_button("Squre", ResPreset.squre),
                                spacing="3",
                                columns="4",
                                width="100%",
                            ),
                        ),
                    ),
                    spacing="3",
                ),
                rx.data_list.root(
                    rx.data_list.item(
                        rx.data_list.label("Ratio"), rx.data_list.value(ResState.ratio)
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Width"),
                        rx.input(
                            placeholder="width",
                            value=ResState.width,
                            on_change=ResState.set_width,
                            size="2",
                            min=0,
                            type="number",
                        ),
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Height"),
                        rx.input(
                            placeholder="height",
                            value=ResState.height,
                            on_change=ResState.set_height,
                            size="2",
                            min=0,
                            type="number",
                        ),
                    ),
                ),
                width="100%",
                align="center",
            ),
        )
    )

    return ui


def preset_button(name, preset) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(f"{name}"),
            rx.text(f"{preset.value.width} x {preset.value.height}"),
            rx.aspect_ratio(
                rx.box(
                    rx.dialog.close(
                        rx.button(
                            f"{preset.value.width_ratio}:{preset.value.height_ratio}",
                            on_click=ResState.set_preset(preset),
                            width="100%",
                            height="100%",
                        ),
                        width="100%",
                        height="100%",
                    ),
                    width="100%",
                    height="100%",
                ),
                ratio=preset.value.width_ratio / preset.value.height_ratio,
            ),
        )
    )
