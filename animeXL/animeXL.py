import reflex as rx
from rxconfig import config
from PIL import Image

from .img.main import gen_image
from .ui.resolution import resolution_ui, ResState
from .ui.general_tag import GeneralTag
from .ui.rating_selector import RatingSelector
from .ui.gender_char_seri import GenderCharactorSeries
from .ui.quality import Quality
from .ui.scale_step import ScaleAndStep
from .ui.negative_tag import NegativeTag


class State(rx.State):
    prompt: str

    is_doing = False

    now_image: Image.Image = None

    is_loading_img = False

    is_first_loading = True

    @rx.event
    async def gen_img(
        self,
        scale,
        step,
        gender,
        char_name,
        series,
        rating,
        general_tags,
        qual1tags,
        qual2tags,
        score_tags,
        negative_tags,
    ):
        if self.is_first_loading == True:
            self.is_first_loading = False
            yield

        res_state = await self.get_state(ResState)

        joiner = ", "

        prom_list = [gender, char_name]

        if series != "":
            prom_list.append(series)

        prom_list.append(rating)

        prom_list.extend(general_tags)

        for tag, is_on in qual1tags:
            if is_on == True:
                prom_list.append(tag)
        for tag, is_on in qual2tags:
            if is_on == True:
                prom_list.append(tag + " quality")
        for tag, is_on in score_tags:
            if is_on == True:
                prom_list.append(tag + " score")

        gened_prompt = joiner.join(prom_list)

        self.prompt = gened_prompt
        yield

        negative_prompt = joiner.join(negative_tags)

        self.is_doing = True
        self.is_loading_img = True
        yield

        try:
            self.now_image = gen_image(
                self.prompt,
                negative_prompt,
                res_state.width,
                res_state.height,
                scale,
                step,
            )
        except:
            self.is_doing = False
            self.is_loading_img = False
            yield
            return

        self.is_loading_img = False
        self.is_doing = False


def index() -> rx.Component:
    general_tag = GeneralTag.create()
    negative_tag = NegativeTag.create()
    rating_selector = RatingSelector.create()
    gender_char_seri = GenderCharactorSeries.create()
    quality = Quality.create()
    scale_and_step = ScaleAndStep.create()

    return rx.flex(
        rx.color_mode.button(position="top-right"),
        rx.flex(
            rx.scroll_area(
                rx.vstack(
                    scale_and_step,
                    resolution_ui(),
                    gender_char_seri,
                    rating_selector,
                    general_tag,
                    quality,
                    negative_tag,
                    rx.card(
                        rx.center(rx.text("Generated Prompt")),
                        rx.text_area(
                            value=State.prompt,
                            on_change=State.set_prompt,
                            read_only=True,
                            size="3",
                            resize="vertical",
                            width="100%",
                        ),
                    ),
                    rx.button(
                        "Generate Image",
                        on_click=State.gen_img(
                            scale_and_step.State.cfg_scale,
                            scale_and_step.State.step,
                            gender_char_seri.State.gender,
                            gender_char_seri.State.c_name,
                            gender_char_seri.State.series,
                            rating_selector.State.rating,
                            general_tag.State.prom_list,
                            quality.State.perfect_tags,
                            quality.State.quality_tags,
                            quality.State.score_tags,
                            negative_tag.State.prom_list,
                        ),
                        loading=State.is_doing,
                        width="100%",
                    ),
                    spacing="3",
                    justify="start",
                    align="stretch",
                    width="98%",
                    height="100%",
                    padding="4",
                ),
                width="40%",
                height="100vh",
            ),
            rx.box(
                rx.cond(
                    State.is_first_loading,
                    rx.card(
                        rx.center(
                            rx.icon("image", size=150, color=rx.color("accent", 5)),
                            width="100%",
                            height="100%",
                        ),
                        width="100%",
                        height="100%",
                    ),
                    rx.skeleton(
                        rx.card(
                            rx.image(
                                src=State.now_image,
                                width="100%",
                                height="100%",
                                object_fit="contain",
                            ),
                            width="100%",
                            height="100%",
                        ),
                        loading=State.is_loading_img,
                        width="100%",
                        height="100%",
                    ),
                ),
                width="60%",
                height="100vh",
                padding="2",
            ),
            direction="row",
            width="100%",
            height="100vh",
            gap="5",
            overflow="hidden",
        ),
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="teal"
    )
)

app.add_page(index)
