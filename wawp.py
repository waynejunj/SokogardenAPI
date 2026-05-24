import requests


class WawpAPI:

    def __init__(self, access_token, instance_id):
        self.access_token = access_token
        self.instance_id = instance_id
        self.base_url = "https://api.wawp.net/v2"

    # -----------------------------------
    # Common request sender
    # -----------------------------------
    def _post(self, endpoint, data=None, files=None):

        url = f"{self.base_url}{endpoint}"

        params = {
            "instance_id": self.instance_id,
            "access_token": self.access_token
        }

        response = requests.post(
            url,
            params=params,
            data=data,
            files=files
        )

        try:
            return response.json()
        except:
            return {
                "status_code": response.status_code,
                "response": response.text
            }

    # -----------------------------------
    # Send text message
    # -----------------------------------
    def send_text(self, number, message):

        data = {
            "chatId": f"{number}@c.us",
            "message": message
        }

        return self._post("/send/text", data=data)

    # -----------------------------------
    # Send image by URL
    # -----------------------------------
    def send_image_url(
        self,
        number,
        image_url,
        filename="image.jpg",
        caption=""
    ):

        data = {
            "chatId": f"{number}@c.us",
            "caption": caption,
            "file[url]": image_url,
            "file[filename]": filename,
            "file[mimetype]": "image/jpeg"
        }

        return self._post("/send/image", data=data)

    # -----------------------------------
    # Send PDF/File by URL
    # -----------------------------------
    def send_file_url(
        self,
        number,
        file_url,
        filename,
        mimetype,
        caption=""
    ):

        data = {
            "chatId": f"{number}@c.us",
            "caption": caption,
            "file[url]": file_url,
            "file[filename]": filename,
            "file[mimetype]": mimetype
        }

        return self._post("/send/file", data=data)

    # -----------------------------------
    # Upload and send local file
    # -----------------------------------
    def send_local_file(
        self,
        number,
        file_path,
        caption=""
    ):

        data = {
            "chatId": f"{number}@c.us",
            "caption": caption
        }

        files = {
            "file": open(file_path, "rb")
        }

        return self._post("/send/file", data=data, files=files)

    # -----------------------------------
    # Send audio
    # -----------------------------------
    def send_audio_url(
        self,
        number,
        audio_url,
        filename="audio.mp3"
    ):

        data = {
            "chatId": f"{number}@c.us",
            "file[url]": audio_url,
            "file[filename]": filename,
            "file[mimetype]": "audio/mpeg"
        }

        return self._post("/send/audio", data=data)

    # -----------------------------------
    # Send video
    # -----------------------------------
    def send_video_url(
        self,
        number,
        video_url,
        filename="video.mp4",
        caption=""
    ):

        data = {
            "chatId": f"{number}@c.us",
            "caption": caption,
            "file[url]": video_url,
            "file[filename]": filename,
            "file[mimetype]": "video/mp4"
        }

        return self._post("/send/video", data=data)

    # -----------------------------------
    # Send buttons
    # -----------------------------------
    def send_buttons(
        self,
        number,
        text,
        buttons
    ):

        data = {
            "chatId": f"{number}@c.us",
            "text": text,
            "buttons": str(buttons)
        }

        return self._post("/send/buttons", data=data)

    # -----------------------------------
    # Send location
    # -----------------------------------
    def send_location(
        self,
        number,
        latitude,
        longitude,
        name="Location",
        address=""
    ):

        data = {
            "chatId": f"{number}@c.us",
            "lat": latitude,
            "lng": longitude,
            "name": name,
            "address": address
        }

        return self._post("/send/location", data=data)

    # -----------------------------------
    # Check session status
    # -----------------------------------
    def session_status(self):

        return self._post("/instance/status")

    # -----------------------------------
    # Logout WhatsApp session
    # -----------------------------------
    def logout(self):

        return self._post("/instance/logout")