from PIL import Image
from math import sqrt
from key_setup import Key
from message_encoder import Message
import sys

class ImagePiece:
    # Keeps track of each image piece and where the next character should be placed
    def __init__(self, start_line, end_line, start_column, end_column):
        self.start_line = start_line
        self.end_line = end_line
        self.start_column = start_column
        self.end_column = end_column
        self.current_line = self.start_line
        self.current_column = self.start_column
        self.full = False

    def isFull(self):
        return self.full

    # Increases position of current (x, y) coordinate
    def increment(self):
        self.current_column += 1
        if self.current_column > self.end_column:
            self.current_column = self.start_column
            self.current_line += 1
        if self.current_line > self.end_line:
            self.full = True

    # Returns the next (x, y) coordinate available
    # for this piece, then increases position of 
    # coordinate
    def get_next_point(self):
        point = [self.current_column, self.current_line]
        self.increment()
        return point


class Order:
    def __init__(self, num_pieces, width, height, lfsr, message_len=0):
        self.num_pieces = num_pieces
        self.pieces = []
        self.width = width
        self.height = height
        self.curr_piece = 0
        self.lfsr = lfsr
        if not sqrt(num_pieces).is_integer():
            raise ValueError('Error: due to current implementation, num_pieces must be square')
        if message_len // 3 > width * height:
            raise ValueError('Error: message too long to fit in given image')

    def set_pieces(self):
        piece_width = int(self.width // sqrt(self.num_pieces))
        piece_height = int(self.height // sqrt(self.num_pieces))
        
        current_column = 0
        current_line = 0

        for i in range(0, self.num_pieces):
            end_column =  current_column + piece_width
            end_line = current_line + piece_height

            if(end_column > self.width):
                current_column = 0
                end_column = current_column + piece_width
                current_line = end_line
                end_line = current_line + piece_height

            self.pieces.append(ImagePiece(current_line, end_line - 1, current_column, end_column - 1)) # -1 since lists start at 0 and end at len -1
            current_column += piece_width

            # Check if there's unassigned columns from last
            # placed piece and add them to it 
            if(self.pieces[-1].end_column + piece_width > self.width):
                self.pieces[-1].end_column = self.width - 1
            
            # Check if there's unassigned lines from last
            # placed piece and add them to it
            
            if(self.pieces[-1].end_line + piece_height > self.height):
                self.pieces[-1].end_line = self.height - 1

    # Increments curr to the next element in pieces,
    # wraps around if it goes out of limit
    def increment_curr(self):
        self.curr_piece += 1
        if self.curr_piece >= len(self.pieces):
            self.curr_piece = 0

    # Increments until we reach the next piece with
    # and empty space
    def get_next_empty(self):
        end_lookup = self.curr_piece - 1
        if self.curr_piece == 0:
            end_lookup = len(self.pieces) -1
        while self.pieces[self.curr_piece].isFull(): # increment until pieces[curr_piece] is not full
            self.increment_curr()
            if self.curr_piece == end_lookup:
                raise ValueError("Error: Image is full. No legal positions found")

    # Uses lfsr to determine porision of next ImagePiece, then
    # iterates until empty piece is found. Returns next available
    # (x,y) coordinate for that piece or raises ValueError if no
    # legal positions are available
    def next(self):
        found = False
        while not found:
            next = self.lfsr.shift() # Check if we want to use current piece
            if(next == 0):
                self.increment_curr() # Increment until we get a piece we want
                continue
            
            self.get_next_empty()
            found = True
            return self.pieces[self.curr_piece].get_next_point()




def modify_value(bit, value):
    if bit == '0' and value % 2 != 0:
        return value - 1
    elif bit == '1' and value % 2 != 1:
        return value + 1
    else:
        return value
    
def encode(num_pieces, message, img):
    k = Key(num_pieces)
    m = Message(message, k)

    private_key = k.get_private_key()

    print("Private key:", private_key)
    print("Ciphertext:", m.ciphertext)
    print("Starting encoding\n")


    im = Image.open(img)
    pixels = im.load()

    order = Order(num_pieces, im.width, im.height, k.lfsr, len(m.ciphertext))
    order.set_pieces()

    # Keep track if we're modifying r, g or b
    # r = 0, g = 1, b = 2
    rgb = 0
    next = order.next()
    for bit in m.ciphertext:
        x = next[0]
        y = next[1]


        val = modify_value(bit, pixels[x, y][rgb])
        if rgb == 0:
            pixels[x, y]= (val, pixels[x, y][1], pixels[x, y][2], pixels[x, y][3])
        elif rgb == 1:
            pixels[x, y]= (pixels[x, y][0], val, pixels[x, y][2], pixels[x, y][3])
        elif rgb == 2:
            pixels[x, y]= (pixels[x, y][0], pixels[x, y][1], val, pixels[x, y][3])


        # Increment rgb, move to next pixel if done with this pixel's b
        rgb += 1
        if rgb > 2:
            rgb = 0
            next = order.next()

    # Save image with no compression
    im.save('./example_image/encoded_img.png', compile=False) # Can change path here
    print("Encoding completed\n")

    return private_key