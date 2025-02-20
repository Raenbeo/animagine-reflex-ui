import reflex as rx


class GenderCharactorSeries(rx.ComponentState):
    gender: str = "1girl"
    c_name: str = "arima kana"
    series: str = "oshi no ko"

    @rx.event
    def change_gender(self, v: str):
        self.gender = v

    @classmethod
    def get_component(cls):
        return rx.card(
            rx.vstack(
                rx.center(
                    rx.heading("Charactor Info"),
                ),
                rx.data_list.root(
                    rx.data_list.item(
                        rx.data_list.label("Gender"),
                        rx.data_list.value(
                            rx.flex(
                                rx.input(value=cls.gender, on_change=cls.set_gender),
                                rx.select(
                                    ["1girl", "1boy", "1other"],
                                    on_change=cls.change_gender,
                                ),
                                direction="row",
                                gap=3,
                            )
                        ),
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Charactor Name"),
                        rx.data_list.value(
                            rx.input(value=cls.c_name, on_change=cls.set_c_name)
                        ),
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Series(Optional)"),
                        rx.data_list.value(
                            rx.input(value=cls.series, on_change=cls.set_series)
                        ),
                    ),
                ),
                width="100%",
                align="center",
            ),
        )
