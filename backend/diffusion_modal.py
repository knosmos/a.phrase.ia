import io
from pathlib import Path

import modal

sdxl_image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install(
        "libglib2.0-0", "libsm6", "libxrender1", "libxext6", "ffmpeg", "libgl1"
    )
    .pip_install(
        "diffusers==0.26.3",
        "invisible_watermark==0.2.0",
        "transformers~=4.38.2",
        "accelerate==0.27.2",
        "safetensors==0.4.2",
    )
)

app = modal.App("stable-diffusion-xl")

with sdxl_image.imports():
    import torch
    from diffusers import DiffusionPipeline
    from fastapi import Response

@app.cls(gpu=modal.gpu.A10G(), container_idle_timeout=240, image=sdxl_image)
class Model:
    @modal.build()
    def build(self):
        from huggingface_hub import snapshot_download

        ignore = [
            "*.bin",
            "*.onnx_data",
            "*/diffusion_pytorch_model.safetensors",
        ]
        snapshot_download(
            "stabilityai/stable-diffusion-xl-base-1.0", ignore_patterns=ignore
        )
        snapshot_download(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            ignore_patterns=ignore,
        )

    @modal.enter()
    def enter(self):
        load_options = dict(
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
            device_map="auto",
        )

        # Load base model
        self.base = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", **load_options
        )

        # Load refiner model
        self.refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=self.base.text_encoder_2,
            vae=self.base.vae,
            **load_options,
        )

        # Compiling the model graph is JIT so this will increase inference time for the first run
        # but speed up subsequent runs. Uncomment to enable.
        # self.base.unet = torch.compile(self.base.unet, mode="reduce-overhead", fullgraph=True)
        # self.refiner.unet = torch.compile(self.refiner.unet, mode="reduce-overhead", fullgraph=True)

    def _inference(self, prompt, n_steps=24, high_noise_frac=0.8):
        negative_prompt = "disfigured, ugly, deformed"
        image = self.base(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=n_steps,
            denoising_end=high_noise_frac,
            output_type="latent",
        ).images
        image = self.refiner(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=image,
        ).images[0]

        byte_stream = io.BytesIO()
        image.save(byte_stream, format="JPEG")

        return byte_stream

    @modal.method()
    def inference(self, prompt, n_steps=24, high_noise_frac=0.8):
        return self._inference(
            prompt, n_steps=n_steps, high_noise_frac=high_noise_frac
        ).getvalue()

    @modal.web_endpoint(docs=True)
    def web_inference(
        self, prompt: str, n_steps: int = 24, high_noise_frac: float = 0.8
    ):
        return Response(
            content=self._inference(
                prompt, n_steps=n_steps, high_noise_frac=high_noise_frac
            ).getvalue(),
            media_type="image/jpeg",
        )

def gen_emoji(description):
    # Stable Diffusion pipeline
    prompt = f"{description} emoji"
    image_bytes = Model().inference.remote(prompt)
    with open("tmp.png", "wb") as f:
        f.write(image_bytes)

    # OpenCV
    dilate_size = 5
    erode_size = 6
    mat = np.array(cv2.imread("tmp.png"))[:,:,::-1]

    canny = cv2.Canny(mat, 200, 100)
    mask = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))

    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cv2.drawContours(mask, [cnt], 0, 255, -1)
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_size, erode_size)))

    img_cv_masked = np.uint8(mat)
    img_cv_masked[mask==0] = 255

    # cv2.imwrite("img_cv.png", img_cv_masked)
    retval, buffer = cv2.imencode('.jpg', img_cv_masked)
    b64_image = base64.b64encode(buffer)

    return b64_image

if __name__ == "__main__":
    print(gen_emoji("an orange water bottle"))