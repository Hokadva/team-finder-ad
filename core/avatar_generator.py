import os
import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .consts import COLORSCHEME, FONTPATH, FONTSIZE, IMAGESIZE, UPOFFSET


def get_font():
    size = FONTSIZE

    for path in FONTPATH:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

        return ImageFont.load_default().font_variant(size=size)


def generate_avatar(user):
    random.seed(user.email)
    background_color, text_color = random.choice(COLORSCHEME)
    random.seed()
    width, height = IMAGESIZE
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    first_letter = user.email[0].upper()
    font = get_font()
    bbox = draw.textbbox((0, 0), first_letter, font=font)
    letter_width = bbox[2] - bbox[0]
    letter_height = bbox[3] - bbox[1]
    centr_x = (width - letter_width) // 2
    centr_y = (height - letter_height) // 2 - UPOFFSET
    draw.text((centr_x, centr_y), first_letter, fill=text_color, font=font)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f'avatar_{user.email.split("@")[0]}_{user.id}.png'
    user.avatar.save(filename, ContentFile(buffer.read()), save=False)
    buffer.close()
