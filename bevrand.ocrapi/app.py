from flask import Flask, jsonify, request
from PIL import Image, ImageOps
from error_model import InvalidUsage
import pytesseract
import base64
import os
import re

application = Flask(__name__)


@application.route('/ping')
def ping_pong():
    return 'pong'


@application.route('/api/v1/base64', methods=['POST'])
def parse_image_from_base64():
    json_body = request.json
    base64_base_string = json_body['base64']
    filename = create_local_image(base64_base_string)

    image = Image.open(filename)

    middle_pixel_colour_dark = get_colour_of_top_left_picture(image)
    grey_image = grey_scale_image(image)
    if middle_pixel_colour_dark is True:
        grey_image = invert_image(grey_image)

    text_in_picture = pytesseract.image_to_string(grey_image)

    os.remove(filename)
    image_text = edit_text(text_in_picture)

    return jsonify({"imageText": image_text, "inverted": middle_pixel_colour_dark}), 200


def get_colour_of_top_left_picture(image):
    width, heigth = image.size
    middle_pixel = width / 2
    pix = image.load()
    colour = pix[middle_pixel, 1]
    pixel_colours = 0
    for c in colour[:3]:
        pixel_colours += c

    avg = pixel_colours / 3

    return bool(avg < 80)


def grey_scale_image(image):
    return image.convert('LA')


def invert_image(image):
    return ImageOps.invert(image.convert('RGB'))


def edit_text(text):
    text_without_illegal_chars = text.replace("‘", "").replace("`", "")
    text_as_array = text_without_illegal_chars.splitlines()
    temp_array = []
    for line in text_as_array:
        if line != "" and line != " " and line != "  ":
            temp_array.append(line)
    return temp_array


def create_local_image(base64_string):
    try:
        base64_base_string = base64_string.split(',')[1]
    except IndexError:
        raise InvalidUsage('Not a valid base64 string', status_code=400, meta=base64_string)
    if re.match("^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$",
                base64_base_string) is None:
        raise InvalidUsage('Not a valid base64 string', status_code=400, meta=base64_base_string)
    image_data = base64.b64decode(base64_base_string)
    if base64_string.startswith('data:image/png;base64,'):
        filename = "{}.png".format(os.getpid())
    elif base64_string.startswith('data:image/jpeg;base64,'):
        filename = "{}.jpg".format(os.getpid())

    with open(filename, 'wb') as f:
        f.write(image_data)

    return filename


@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    application.run()
