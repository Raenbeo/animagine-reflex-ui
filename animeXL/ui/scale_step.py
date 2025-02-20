import reflex as rx


class ScaleAndStep(rx.ComponentState):
    cfg_scale: int = 5
    step: int = 28

    @classmethod
    def get_component(cls):
        return rx.card(
            rx.vstack(
                rx.center(
                    rx.heading("Sacle Step"),
                ),
                rx.data_list.root(
                    rx.data_list.item(
                        rx.data_list.label("CFG Scale : 4-7 (Recommended : 5)"),
                        rx.data_list.value(
                            rx.input(
                                value=cls.cfg_scale,
                                on_change=cls.set_cfg_scale,
                                type="number",
                            ),
                        ),
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Sampling Steps : 25~28 (Recommended : 28)"),
                        rx.data_list.value(
                            rx.input(
                                value=cls.step, on_change=cls.set_step, type="number"
                            )
                        ),
                    ),
                ),
                width="100%",
                align="center",
            ),
        )
