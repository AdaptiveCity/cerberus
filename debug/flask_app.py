from flask import Flask, send_file, Response
import os
import subprocess
from io import BytesIO
import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

app = Flask(__name__)
PORT=8899

def add_timestamp_to_image(image_data):
    # Load the image
    img = Image.open(BytesIO(image_data))

    # Get the current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Define the font and its size
    font = ImageFont.truetype("../fonts/arial.ttf", 20)

    # Create a draw object
    draw = ImageDraw.Draw(img)

    # Define the text color (white) and position
    text_color = (255, 255, 255)
    position = (10, 10)

    # Add the timestamp to the image
    draw.text(position, current_time, fill=text_color, font=font)

    # Save the image to a BytesIO object
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)

    return output

def get_address():
    # Define the command as a list of its parts
    command = ["hostname", "-I"]

    # Run the command and store the output
    output = subprocess.check_output(command)

    # Convert the output from bytes to a string and remove any trailing whitespace
    hostname_ip = output.decode("utf-8").strip()

    # Print the result
    #rint("Hostname IP:", hostname_ip)
    print("\n===============================")
    print("Access the camera at:",hostname_ip+"\t:"+str(PORT)+'/show_img')
    print("===============================\n")


@app.route('/show_img')
def show_img():
    # Run the shell command
    cmd = "libcamera-still --timelapse 1000 --output test.jpg"
    subprocess.run(cmd, shell=True, check=True)

    # Wait for the test.jpg file to be created
    while not os.path.exists("test.jpg"):
        time.sleep(1)

    # Load the image and send it as a response
    with open("test.jpg", "rb") as img_file:
        img_data = img_file.read()

    # Add a timestamp to the image
    img_with_timestamp = add_timestamp_to_image(img_data)

    # Clean up by deleting the test.jpg file
    os.remove("test.jpg")

    # Send the image with the timestamp as a response
    return send_file(img_with_timestamp, mimetype='image/jpeg')


if __name__ == '__main__':
    get_address()
    app.run(host='0.0.0.0', port=PORT)
