import io
from PIL import Image, ImageDraw, ImageFont
import os
from colorthief import ColorThief
from django.conf import settings


class ThumbNailCreator(object):

    MYSOC_BLUE = (79, 173, 237)
    MYSOC_GREEN = (98, 179, 86)
    MYSOC_RED = (224, 75, 75)
    MYSOC_VIOLET = (169, 76, 166)
    MYSOC_ORANGE = (241, 161, 64)
    MYSOC_YELLOW = (255, 216, 54)
    MYSOC_OFF_WHITE = (243, 241, 235)
    MYSOC_LIGHT_GREY = (226, 223, 217)
    MYSOC_DARK_GREY = (108, 107, 104)
    MYSOC_BLACK = (51, 51, 51)

    BLOG = "B"
    REPORT = "R"
    POLICY = "P"
    CONSULTATION = "C"
    MINISITE = "M"

    mysoc_colors = [MYSOC_BLUE,
                    MYSOC_GREEN,
                    MYSOC_RED,
                    MYSOC_VIOLET,
                    MYSOC_ORANGE,
                    MYSOC_YELLOW,
                    MYSOC_OFF_WHITE,
                    MYSOC_LIGHT_GREY,
                    MYSOC_DARK_GREY,
                    MYSOC_BLACK]

    writing_colours = [MYSOC_OFF_WHITE,
                       MYSOC_BLACK]

    font_location = settings.THUMBNAIL_FONT

    @classmethod
    def color_distance(cls, rgb1, rgb2):
        """
        calculate distance between two colors
        https://stackoverflow.com/a/8863926
        """
        rm = 0.5 * (rgb1[0] + rgb2[0])
        rd = ((2 + rm) * (rgb1[0] - rgb2[0])) ** 2
        gd = (4 * (rgb1[1] - rgb2[1])) ** 2
        bd = ((3 - rm) * (rgb1[2] - rgb2[2])) ** 2
        dist = (rd + gd + bd) ** 0.5
        return dist

    @classmethod
    def convert_hero_image_to_thumbnail(cls,
                                        source,
                                        dest=None,
                                        text=BLOG,
                                        color_match_quality=1):
        """
        expects an image roughly 1024x 680
        creates a thumbnail
        if no destination - returns a file objecct
        """
        img = Image.open(source)

        # get the complimentary colour for the background
        color_thief = ColorThief(source)
        color = color_thief.get_color(quality=color_match_quality)

        base_image = Image.new('RGB', (110, 150), color=color)

        ratio = img.width / 110
        new_height = img.height / ratio
        img = img.resize((110, new_height), Image.BICUBIC)

        base_image.paste(img, (0, 150 / 2 - (new_height / 2) + 20))

        # find best writing color for background
        cls.writing_colours.sort(
            key=lambda x: cls.color_distance(x, color), reverse=True)
        font_color = cls.writing_colours[0]

        draw = ImageDraw.Draw(base_image)
        if text == cls.BLOG:
            font = ImageFont.truetype(cls.font_location, 40)
            draw.text((14, 0), "blog", font_color, font=font)
        if text == cls.REPORT:
            font = ImageFont.truetype(cls.font_location, 35)
            draw.text((6, 0), "report", font_color, font=font)
        if text == cls.POLICY:
            font = ImageFont.truetype(cls.font_location, 35)
            draw.text((9, 0), "policy", font_color, font=font)
        if text == cls.CONSULTATION:
            font = ImageFont.truetype(cls.font_location, 18)
            draw.text((5, 5), "consultation", font_color, font=font)
            draw.text((19, 22), "response", font_color, font=font)
        if text == cls.MINISITE:
            font = ImageFont.truetype(cls.font_location, 30)
            draw.text((24, -1), "mini", font_color, font=font)
            draw.text((31, 25), "site", font_color, font=font)

        if dest:
            base_image.save(dest, quality=95)
        else:
            b = io.BytesIO()
            base_image.save(b, "png")
            b.seek(0)
            return b

    @classmethod
    def convert_folder(cls, source_folder, dest_folder):
        """
        convert all images in a source folder
        to a thumbnail in the new folder
        """
        for f in os.listdir(source_folder):
            origin = os.path.join(source_folder, f)
            dest_file = os.path.join(dest_folder, f)
            cls.convert_hero_image_to_thumbnail(origin, dest_file)