import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

pipe = StableDiffusionPipeline.from_pretrained(
    "valhalla/emoji-diffusion",
    torch_dtype=torch.float16,
).to("cuda")
euler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
pipe.scheduler = euler

def gen_emoji(description):
    prompt = f"{description} emoji"
    images = pipe(prompt, num_inference_steps=30).images
    print(len(images))
    images[0].save("tmp.png")

if __name__ == "__main__":
    print(gen_emoji("orange water bottle"))