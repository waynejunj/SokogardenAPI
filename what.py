from flask import Flask, request, jsonify
from flask_cors import CORS
from wawp import WawpAPI
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# -----------------------------------
# WAWP CONFIG
# -----------------------------------

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
INSTANCE_ID = os.getenv("INSTANCE_ID")

client = WawpAPI(ACCESS_TOKEN,INSTANCE_ID)

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "WAWP Flask API Running"
    })


# -----------------------------------
# SEND TEXT
# -----------------------------------

@app.route("/send-text", methods=["POST"])
def send_text():

    try:

        data = request.form

        number = data.get("number")
        message = data.get("message")

        response = client.send_text(number,message)

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND IMAGE URL
# -----------------------------------

@app.route("/send-image-url", methods=["POST"])
def send_image_url():

    try:

        data = request.form

        number = data.get("number")
        image_url = data.get("image_url")
        caption = data.get("caption", "")

        response = client.send_image_url(
            number,
            image_url,
            caption=caption
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND FILE URL
# -----------------------------------

@app.route("/send-file-url", methods=["POST"])
def send_file_url():

    try:

        data = request.form

        number = data.get("number")
        file_url = data.get("file_url")
        filename = data.get("filename")
        mimetype = data.get("mimetype")
        caption = data.get("caption", "")

        response = client.send_file_url(
            number,
            file_url,
            filename,
            mimetype,
            caption
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND LOCAL FILE
# -----------------------------------

@app.route("/send-local-file", methods=["POST"])
def send_local_file():

    try:

        number = request.form.get("number")
        caption = request.form.get("caption", "")

        uploaded_file = request.files["file"]

        # Create uploads folder
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        filepath = os.path.join(
            "uploads",
            uploaded_file.filename
        )

        uploaded_file.save(filepath)

        response = client.send_local_file(
            number,
            filepath,
            caption
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND AUDIO
# -----------------------------------

@app.route("/send-audio", methods=["POST"])
def send_audio():

    try:

        data = request.form

        number = data.get("number")
        audio_url = data.get("audio_url")

        response = client.send_audio_url(
            number,
            audio_url
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND VIDEO
# -----------------------------------

@app.route("/send-video", methods=["POST"])
def send_video():

    try:

        data = request.form

        number = data.get("number")
        video_url = data.get("video_url")
        caption = data.get("caption", "")

        response = client.send_video_url(
            number,
            video_url,
            caption=caption
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND BUTTONS
# -----------------------------------

@app.route("/send-buttons", methods=["POST"])
def send_buttons():

    try:

        data = request.form

        number = data.get("number")
        text = data.get("text")

        buttons = [
            {
                "id": "btn1",
                "text": "Yes"
            },
            {
                "id": "btn2",
                "text": "No"
            }
        ]

        response = client.send_buttons(
            number,
            text,
            buttons
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SEND LOCATION
# -----------------------------------

@app.route("/send-location", methods=["POST"])
def send_location():

    try:

        data = request.form

        number = data.get("number")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        name = data.get("name")
        address = data.get("address")

        response = client.send_location(
            number,
            latitude,
            longitude,
            name,
            address
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# SESSION STATUS
# -----------------------------------

@app.route("/session-status", methods=["GET"])
def session_status():

    try:

        response = client.session_status()

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# LOGOUT
# -----------------------------------

@app.route("/logout", methods=["POST"])
def logout():

    try:

        response = client.logout()

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------------
# RUN SERVER
# -----------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )