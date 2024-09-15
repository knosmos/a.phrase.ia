import requests
import io
import base64
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def gen_emoji(description, cv_postprocess=False):
    image_bytes = query({
        "inputs": description + ", realistic shading, white blank background",
    })
    image = Image.open(io.BytesIO(image_bytes))
    image.save("tmp.png")

    if cv_postprocess:
        dilate_size = 5
        erode_size = 6
        mat = np.array(image)[:,:,::-1]

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

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("u8")
    return img_str

if __name__ == "__main__":
    gen_emoji(input())