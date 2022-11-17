import string


def get_font_height(font):
    return font.size(string.printable)[1]


def crop_bb_to_fit(bb, bb_to_fit):
    if bb.x < bb_to_fit.x:
        bb.width += bb.x - bb_to_fit.x
        bb.x = bb_to_fit.x
    if bb.x + bb.width > bb_to_fit.x + bb_to_fit.width:
        bb.width = bb_to_fit.x + bb_to_fit.width - bb.x
        bb.x = bb_to_fit.x + bb_to_fit.width - bb.width
    if bb.y < bb_to_fit.y:
        bb.height += bb.y - bb_to_fit.y
        bb.y = bb_to_fit.y
    if bb.y + bb.height > bb_to_fit.y + bb_to_fit.height:
        bb.height = bb_to_fit.y + bb_to_fit.height - bb.y
        bb.y = bb_to_fit.y + bb_to_fit.height - bb.height
    return bb
