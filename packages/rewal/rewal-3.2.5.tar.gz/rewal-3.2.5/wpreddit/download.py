import os.path
import re
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
from urllib import request

from wpreddit import config


# credit: http://www.techniqal.com/blog/2011/01/18/python-3-file-read-write-with-urllib/
# in - string - direct url of the image to download
# out - Image - image
# downloads the specified image and saves it to disk
def download_image(url, title):
    uaurl = request.Request(url, headers={'User-Agent': 'wallpaper-reddit python script by /u/MarcusTheGreat7'})
    f = request.urlopen(uaurl)
    print("downloading " + url)
    try:
        img = Image.open(f).convert('RGB')
        if config.resize:
            config.log("resizing the downloaded wallpaper")
            img = ImageOps.fit(img, (config.minwidth, config.minheight), Image.ANTIALIAS)
        if config.settitle:
            img = set_image_title(img, title)
        if config.opsys == "Windows":
            file_path = os.path.join(config.walldir, os.path.basename(url).split('.')[0] + ".bmp")
            img.save(file_path, "BMP")
            return file_path
        else:
            file_path = os.path.join(config.walldir, os.path.basename(url).split('.')[0] + '.jpg')
            img.save(file_path, "JPEG")
            return file_path

    except IOError as ex:
        print("Error saving image!", ex)
        sys.exit(1)


# in - string, string - path of the image to set title on, title for image
def set_image_title(img, title):
    config.log("setting title")
    title = remove_tags(title)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(config.walldir + '/fonts/Cantarell-Regular.otf', size=config.titlesize)
    x = 0
    y = 0
    if config.titlealign_x == "left":
        x = config.titleoffset_x
    elif config.titlealign_x == "center":
        text_x = font.getsize(title)[0]
        x = (img.size[0] - text_x)/2
    elif config.titlealign_x == "right":
        text_x = font.getsize(title)[0]
        x = img.size[0] - text_x - config.titleoffset_x
    if config.titlealign_y == "top":
        y = config.titleoffset_y
    elif config.titlealign_y == "bottom":
        text_y = font.getsize(title)[1]
        y = img.size[1] - text_y - config.titleoffset_y
    draw.text((x+2, y+2), title, font=font, fill=(0, 0, 0, 127))
    draw.text((x, y), title, font=font)
    del draw
    return img


# in - [string, string, string] - url, title, and permalink
# saves the url of the image to ~/.wallpaper/url.txt, the title of the image to ~/.wallpaper/title.txt,
# and the permalink to ~/.wallpaper/permalink.txt just for reference
def save_info(link):
    # Reddit escapes the unicode in json, so when the json is downloaded, the info has to be manually re-encoded
    # and have the unicode characters reprocessed
    # title = title.encode('utf-8').decode('unicode-escape')
    with open(config.walldir + '/url.txt', 'w') as urlinfo:
        urlinfo.write(link[0])
    with open(config.walldir + '/title.txt', 'w') as titleinfo:
        titleinfo.write(remove_tags(link[1]))
    with open(config.walldir + '/permalink.txt', 'w') as linkinfo:
        linkinfo.write(link[2])


# in - string - title of the picture
# out - string - title without any annoying tags
# removes the [tags] throughout the image
def remove_tags(str):
    return re.sub(' +', ' ', re.sub("[\[\(\<].*?[\]\)\>]", "", str)).strip()
