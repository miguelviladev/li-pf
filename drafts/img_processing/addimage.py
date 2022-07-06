from PIL import Image, ImageFilter
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os
import io

#Transform image to bytes
def TransformToBytes(data):
    image = open(data, 'rb')
    return image.read()



#cipher image represented in bytes
def cipherimage(data):
    key= b'NarcisosNarcisos'
    cipher= AES.new(key, AES.MODE_ECB)
    dataencrypted= cipher.encrypt(data)
    
    return dataencrypted

def hashimage(img):
    hash = SHA256.new()
    hash.update(img)
    return hash.hexdigest()
    
    
    # image = Image.open(io.BytesIO(dataencrypted))
    # image.show()
    # image.save("cipher.png")
    

   
img = Image.open('watermark.jpg').convert('RGBA')
img.putalpha(130) 
img.save('logoxImagens.png')

input_image_path = 'sapce.jpg'
watermark_image_path = 'logoxImagens.png'
output_image_path = 'gato_watermarked.png'

def watermark(input_image_path, output_image_path, watermark_image_path):
    base_image = Image.open(input_image_path).convert('RGBA')
    watermark = Image.open(watermark_image_path).convert('RGBA')
    watermark_ratio = watermark.size[1] / watermark.size[0]
    
    watermark.thumbnail((int((0.2 * base_image.size[0])), int(base_image.size[1] * watermark_ratio)))

    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0,0,0,0))
    transparent.paste(base_image, (0,0))
    position=(int(width / 2 - watermark.size[0] / 2), int(height / 2 - watermark.size[1] / 2))
    transparent.paste(watermark, position, mask=watermark)
    transparent.show()
    transparent.save(output_image_path)

def main():
    img = input_image_path
    
    # watermark(img, output_image_path, watermark_image_path)
    # main(input_image_path)
    
    
    img = Image.open(input_image_path)
    width, height = img.size
    print("Largura: %dpx" % width)
    print("Altura: %dpx" % height)
    print("Formato: %s" % img.format)
    
    imgbytes = TransformToBytes(input_image_path)  
    cipherimage(imgbytes)
    print(hashimage(imgbytes))
main()