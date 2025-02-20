import reflex as rx


init_perfect_tags: list[tuple[str, bool]] = [
    ("masterpiece", True),
    ("absurdres", True),
]
init_quality_tags: list[tuple[str, bool]] = [
    ("best", False),
    ("low", False),
    ("worst", False),
]
init_score_tags: list[tuple[str, bool]] = [
    ("high", True),
    ("greet", True),
    ("good", False),
    ("average", False),
    ("bad", False),
    ("low", False),
]


class Quality(rx.ComponentState):
    perfect_tags: list[tuple[str, bool]] = init_perfect_tags.copy()
    quality_tags: list[tuple[str, bool]] = init_quality_tags.copy()
    score_tags: list[tuple[str, bool]] = init_score_tags.copy()

    @rx.event
    def perfect_change(self, name, is_on, idx):
        item = self.perfect_tags[idx]
        new_item = (name, not is_on)
        self.perfect_tags[idx] = new_item

    @rx.event
    def qual_change(self, name, is_on, idx):
        item = self.quality_tags[idx]
        new_item = (name, not is_on)
        self.quality_tags[idx] = new_item

    @rx.event
    def score_change(self, name, is_on, idx):
        item = self.score_tags[idx]
        new_item = (name, not is_on)
        self.score_tags[idx] = new_item

    @rx.event
    def reset_to_recommend(self):
        self.perfect_tags = init_perfect_tags.copy()
        self.quality_tags = init_quality_tags.copy()
        self.score_tags = init_score_tags.copy()

    @classmethod
    def get_component(cls):
        return rx.card(
            rx.vstack(
                rx.center(
                    rx.heading("Quality And Score"),
                    rx.button("Reset To Recommend", on_click=cls.reset_to_recommend),
                    spacing="3",
                ),
                rx.card(
                    rx.center(rx.text("Quality")),
                    rx.center(
                        rx.flex(
                            rx.foreach(
                                cls.perfect_tags,
                                lambda tag, idx: perfect_switch(
                                    cls, tag[0], tag[1], idx
                                ),
                            ),
                            rx.foreach(
                                cls.quality_tags,
                                lambda tag, idx: quality_switch(
                                    cls, tag[0], tag[1], idx
                                ),
                            ),
                            gap=7,
                            direction="row",
                            flex_wrap="wrap",
                        ),
                        align="center",
                        justify="center",
                    ),
                ),
                rx.card(
                    rx.center(rx.text("Score")),
                    rx.center(
                        rx.flex(
                            rx.foreach(
                                cls.score_tags,
                                lambda tag, idx: score_switch(cls, tag[0], tag[1], idx),
                            ),
                            gap=7,
                            direction="row",
                            flex_wrap="wrap",
                        ),
                        align="center",
                        justify="center",
                    ),
                ),
                width="100%",
                align="center",
            ),
        )


def perfect_switch(cls, name, is_on, idx):
    return rx.card(
        rx.vstack(
            rx.text(name),
            rx.switch(checked=is_on, on_change=cls.perfect_change(name, is_on, idx)),
            align="center",
        ),
        on_click=cls.perfect_change(name, is_on, idx),
    )


def quality_switch(cls, name, is_on, idx):
    return rx.card(
        rx.vstack(
            rx.text(name),
            rx.switch(checked=is_on, on_change=cls.qual_change(name, is_on, idx)),
            align="center",
        ),
        on_click=cls.qual_change(name, is_on, idx),
    )


def score_switch(cls, name, is_on, idx):
    return rx.card(
        rx.vstack(
            rx.text(name),
            rx.switch(checked=is_on, on_change=cls.score_change(name, is_on, idx)),
            align="center",
        ),
        on_click=cls.score_change(name, is_on, idx),
    )
