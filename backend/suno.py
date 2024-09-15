import requests

API_URL = "https://studio-api.suno.ai/api/external/generate"
headers = {"Authorization": "Bearer FleOqDtGzPeAsWP273YwvVRdzVEyRkjr"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response)
    return response.json()

def send_song(lyrics):
    resp = query({
        "topic": lyrics,
        "tags": "pop",
        "mv": "chirp-v3-5"
    })
    print(resp)
    return resp.id

if __name__ == "__main__":
    print(send_song("let's go and fetch our decentralized cloud based agent ai"))