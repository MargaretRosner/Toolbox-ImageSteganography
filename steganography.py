"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    img = red_channel.load()
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    #in order to get the things you have to conver the number int binary
    for x in range(x_size):
        for y in range(y_size):
            pixel = img[x,y]
            binary_pixel = bin(pixel)
            if binary_pixel[-1] == '1':
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)
    decoded_image.save("/home/maggie/Desktop/Toolbox-ImageSteganography/images/decoded_image.png")

#decode_image()


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    #calc size of the image
    im = Image.open(template_image)
    size = im.size
    preencoded_image = write_text(text_to_encode,size)

    # im2 = Image.open(preencoded_image)

    red_channel2 = im.split()[0]
    img2 = red_channel2.load()
    x_size2 = size[0]
    y_size2 = size[1]


    red_channel = preencoded_image.split()[0]
    img = red_channel.load()
    x_size = preencoded_image.size[0]
    y_size = preencoded_image.size[1]


    almostdecoded_image = Image.new("RGB", preencoded_image.size)
    pixels = almostdecoded_image.load()

    for x in range(x_size):
        for y in range(y_size):
            pixela = img[x,y]#image with the message
            pixelb = img2[x,y]#image without the message
            binary_pixel_a = bin(pixela)
            binary_pixel_b = bin(pixelb)
            if pixela > 0:
                print(pixela)
                print(binary_pixel_a)

            if binary_pixel_a[-1] == '1':
                #sets 1st pixel on right of the actual image to 1 if the pixel in the image encoded with text is 1 there
                binary_pixel_b[-1] == '1'
            else:
                #sets 1st pixel on right of the actual image to 1 if the pixel in the image encoded with text is 1 there
                binary_pixel_b[-1] == 0
            r, g, b = im.load()[x, y]
            pixels[x, y] = (int(binary_pixel_b, 2), g, b)
    almostdecoded_image.save("/home/maggie/Desktop/Toolbox-ImageSteganography/images/encode_image.png")
    #pass #TODO: Fill out this function. how do you change a value to be zero or one only if it matches the encoded image

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image("hello")
