import reflex as rx


class RatingSelector(rx.ComponentState):
    rating_list: list[str] = ["safe", "sensitive", "nsfw", "explicit"]

    rating: str = rating_list[0]

    @rx.event
    def set_rating(self, rate):
        self.rating = rate

    @classmethod
    def get_component(cls):
        return rx.card(
            rx.vstack(
                rx.center(
                    rx.heading("Rating"),
                ),
                rx.radio(
                    cls.rating_list,
                    value=cls.rating,
                    on_change=cls.set_rating,
                    direction="row",
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
