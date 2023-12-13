from image_decoding import decode
from image_encoding import encode


text = "The Weird Sisters hand in hand Posters of the sea and land Thus do go about about Thrice to thine and thrice to mine And thrice again to make up nine. Peace the charms wound up. Lesser than Macbeth and greater. Not so happy yet much happier. Thou shalt get king though thou be none. So all hail Macbeth and Banquo. Banquo and Macbeth all hail"

private_key = encode(16, text, './example_image/img.png')
decode(private_key, './example_image/encoded_img.png')