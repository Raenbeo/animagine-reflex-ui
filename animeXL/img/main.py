import torch
from diffusers import StableDiffusionXLPipeline

import gc
from datetime import datetime


def gen_image(prompt, negative_prompt, width, height, cfg_scale, sampling_steps):
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "cagliostrolab/animagine-xl-4.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
        custom_pipeline="lpw_stable_diffusion_xl",
        add_watermarker=False,
    )
    pipe.to("cuda")

    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        guidance_scale=cfg_scale,
        num_inference_steps=sampling_steps,
    ).images[0]

    del pipe
    gc.collect()
    torch.cuda.empty_cache()

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    image.save(f"./output/{current_time}.png")

    return image
