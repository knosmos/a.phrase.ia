# import torch
# import cv2
# import numpy as np
# import base64
# from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

# pipe = StableDiffusionPipeline.from_pretrained(
#     "valhalla/emoji-diffusion",
#     # "Mobius-labs/emoji_model_msfluentui",
#     # "CompVis/stable-diffusion-v1-4",
#     torch_dtype=torch.float16,
# ).to("cuda")
# euler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
# pipe.scheduler = euler

# def gen_emoji(description):
#     # Stable Diffusion pipeline
#     prompt = f"{description} emoji"
#     image = pipe(prompt, num_inference_steps=30).images[0]
#     # image.save("tmp.png")

#     # OpenCV
#     dilate_size = 5
#     erode_size = 6
#     mat = np.array(image)[:,:,::-1]

#     canny = cv2.Canny(mat, 200, 100)
#     mask = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))
#     mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))

#     contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#     for cnt in contours:
#         cv2.drawContours(mask, [cnt], 0, 255, -1)
#     mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_size, erode_size)))

#     img_cv_masked = np.uint8(mat)
#     img_cv_masked[mask==0] = 255

#     # cv2.imwrite("img_cv.png", img_cv_masked)
#     retval, buffer = cv2.imencode('.jpg', img_cv_masked)
#     b64_image = base64.b64encode(buffer)

#     return b64_image

# if __name__ == "__main__":
#     print(gen_emoji("an orange water bottle"))