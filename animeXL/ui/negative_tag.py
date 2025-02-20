import reflex as rx

recommend_prompt_list = [
    "lowres",
    "bad anatomy",
    "bad hands",
    "text",
    "error",
    "missing finger",
    "extra digits",
    "fewer digits",
    "cropped",
    "worst quality",
    "low quality",
    "low score",
    "bad score",
    "average score",
    "signature",
    "watermark",
    "username",
    "blurry",
    "logo",
]


class NegativeTag(rx.ComponentState):
    prom_list: list[str] = recommend_prompt_list.copy()
    recommend_list: list[str] = recommend_prompt_list.copy()

    tag: str

    @rx.event
    def prom_list_reset(self):
        self.prom_list = self.recommend_list.copy()

    @rx.event
    def delete_prom(self, idx):
        self.prom_list.pop(idx)

    @rx.event
    def add_prom(self, key):
        if key == "Enter" and self.tag != "":
            self.prom_list.append(self.tag)
            self.tag = ""

    @classmethod
    def get_component(cls):
        return rx.card(
            rx.vstack(
                rx.center(
                    rx.heading(f"Negative Tags ({cls.prom_list.length()})"),
                    rx.button("Reset To Recommend", on_click=cls.prom_list_reset),
                    spacing="3",
                ),
                rx.flex(
                    rx.foreach(cls.prom_list, lambda name, idx: badge(cls, name, idx)),
                    gap=4,
                    direction="row",
                    flex_wrap="wrap",
                ),
                rx.input(
                    placeholder="write tag and enter to add",
                    value=cls.tag,
                    on_change=cls.set_tag,
                    on_key_up=cls.add_prom,
                    width="100%",
                ),
                width="100%",
                align="center",
            ),
        )


def badge(cls, prom, idx):
    return rx.card(
        rx.popover.root(
            rx.popover.trigger(rx.center(rx.text(prom))),
            rx.popover.content(
                rx.center(
                    rx.popover.close(rx.button("Delete", on_click=cls.delete_prom(idx)))
                )
            ),
        )
    )
