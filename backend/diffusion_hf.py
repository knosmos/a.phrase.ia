import requests
import io
import cv2
import base64
import numpy as np
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {open('.api_key_hf').read()}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def gen_emoji(description, cv_postprocess=False):
    image_bytes = query({
        "inputs": description + ", realistic shading, white blank background",
    })
    image = Image.open(io.BytesIO(image_bytes))
    image.save("tmp.png")

    dilate_size = 5
    erode_size = 6
    mat = np.array(image)[:,:,::-1]

    canny = cv2.Canny(mat, 200, 100)
    mask = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_size, dilate_size)))

    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if cv_postprocess:
        for cnt in contours:
            cv2.drawContours(mask, [cnt], 0, 255, -1)
        mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode_size, erode_size)))

        img_cv_masked = np.uint8(mat)
        img_cv_masked[mask==0] = 255

        # cv2.imwrite("img_cv.png", img_cv_masked)
        retval, buffer = cv2.imencode('.jpg', img_cv_masked)
        b64_image = base64.b64encode(buffer)

        return b64_image

    # crop and pad
    largest_contour = None
    largest_contour_area = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > largest_contour_area:
            largest_contour_area = cv2.contourArea(cnt)
            largest_contour = cv2.boundingRect(cnt)
    x, y, w, h = largest_contour
    roi = mat[y: y + h, x: x + w]
    s = max(w, h)
    result = np.full((s, s, 3), (255, 255, 255), dtype=np.uint8)
    x_center = (s - w) // 2
    y_center = (s - h) // 2
    result[y_center:y_center+h, 
        x_center:x_center+w] = roi

    cv2.imwrite("roi.jpg", result)
    retval, buffer = cv2.imencode('.jpg', roi)
    b64_image = base64.b64encode(buffer)
    return b64_image

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("u8")
    return img_str

if __name__ == "__main__":
    gen_emoji(input())