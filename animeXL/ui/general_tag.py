import reflex as rx


class GeneralTag(rx.ComponentState):
    prom_list: list[str] = [
        "cosplay",
        "looking at viewer",
        "smile",
        "outdoors",
        "night",
        "v",
    ]

    tag: str

    prompt: str

    @rx.event
    def prompt2tags(self, v):
        tags = v.split(", ")
        self.prom_list = tags
        self.prompt = ""

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
                    rx.heading(f"General Tags ({cls.prom_list.length()})"),
                    rx.dialog.root(
                        rx.dialog.trigger(rx.button("prompt2tags")),
                        rx.dialog.content(
                            rx.dialog.title("Prompt To Tags"),
                            rx.dialog.description(
                                "Change Your Prompt To Tags.",
                                size="2",
                                margin_bottom="16px",
                            ),
                            rx.text_area(
                                value=cls.prompt,
                                on_change=cls.set_prompt,
                                width="100%",
                                height="100%",
                            ),
                            rx.flex(
                                rx.dialog.close(
                                    rx.button(
                                        "Cancel",
                                        color_scheme="gray",
                                        variant="soft",
                                    ),
                                ),
                                rx.dialog.close(
                                    rx.button(
                                        "Trans", on_click=cls.prompt2tags(cls.prompt)
                                    ),
                                ),
                                spacing="3",
                                margin_top="16px",
                                justify="end",
                            ),
                        ),
                    ),
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
