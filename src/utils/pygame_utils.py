import string


def get_font_height(font):
    return font.size(string.printable)[1]
