from image_encoding import Order, ImagePiece
from lfsr import LFSR
from key_setup import Key, Node
from PIL import Image

def read_rgb(rgb):
    return str(rgb % 2)

def decode(private_key, img):
    # Create a new key and flip dic keys/values for easier access
    k = Key(private_key[0], private_key[1], private_key[2], private_key[3])
    k.values = {values: key for key, values in k.values.items()}

    im = Image.open(img)
    pixels = im.load()

    order = Order(k.num_pieces, im.width, im.height, k.lfsr)
    order.set_pieces()

    rgb = 0
    next = order.next()
    msg = ''
    code_word = ''
    max_length = max(map(len, k.values))


    try:
        # Will run until we get a value error 
        # either because we reached a value 
        # that's not recognized or because we
        # traversed all pixels
        while(True): 
            x = next[0]
            y = next[1]

            bit = read_rgb(pixels[x, y][rgb])
            code_word += bit
            
            # If codeword is in dictionnary,
            # Add letter to dictionnary and
            # Reset it. If it's end of text
            # marker, stop the code
            if code_word in k.values:
                if k.values[code_word] == '!':
                    raise ValueError('Error: code_word not recognized')
                msg += k.values[code_word]
                code_word=''
            
            if len(code_word) > max_length:
                raise ValueError('Error: code_word not recognized')

            # Increment rgb, move to next pixel if
            # done with this pixel
            rgb += 1
            if rgb > 2:
                rgb = 0
                next = order.next()
    except ValueError:
        print(msg)
        return msg
