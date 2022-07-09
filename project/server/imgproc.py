import base64
import sys
import os
import io
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from config import *

def hashImage(base64_img):
    hash = SHA256.new()
    hash.update(base64_img.encode('utf-8'))
    return hash.hexdigest()

def encryptImage(content):
    return AES.new(KEY, AES.MODE_ECB).encrypt(pad(content, BLOCKSIZE))

def decryptImage(content):
    return unpad(AES.new(KEY, AES.MODE_ECB).decrypt(content), BLOCKSIZE)

def writeImage(content, filename):
    with open(filename, "wb") as file:
        file.write(base64.b64decode(content))

def writeWatermarkedImage(input_image_path, output_image_path, watermark_image_path, text = ""):
    base_image = Image.open(input_image_path).convert('RGBA')
    watermark = Image.open(watermark_image_path).convert('RGBA')
    width, height = base_image.size
    watermark_ratio = watermark.size[1] / watermark.size[0]
    watermark.thumbnail((int((0.2 * base_image.size[0])), int(base_image.size[1] * watermark_ratio)))

    shape = Image.new("RGBA", (width, int(2 * watermark.size[1])), (0, 0, 0, 100))

    shape.save("shape.png")

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    
    # posicao da shape
    position = (0, int(height / 2 - shape.size[1] / 4))
    transparent.paste(shape, position, mask=shape)
    transparent.save(output_image_path)
    
    # posicao da logo
    position2 = (int(width / 2 - watermark.size[0] / 2), int(height / 2 - watermark.size[1] / 2))
    transparent.paste(watermark, position2, mask=watermark)
    transparent.save(output_image_path)

    color = (255, 255, 255)
    text = "OWNER INFO"
    
    fontsize = 1
    img_fraction = 0.75

    font = ImageFont.truetype(FONT, fontsize)
    while font.getsize(text)[0] < img_fraction*base_image.size[0] and font.getsize(text)[1] < watermark.height / 2:
        fontsize += 1
        font = ImageFont.truetype(FONT, fontsize)
        
    fontsize -= 1
    
    draw = ImageDraw.Draw(transparent)
    position = (int(width/2-font.getsize(text)[0]/2), int(height/2-font.getsize(text)[1]/2 + watermark.size[1]/2 + watermark.size[1] / 2))
    
    draw.text(position, text, fill=color, font=font)
    transparent.save(output_image_path)