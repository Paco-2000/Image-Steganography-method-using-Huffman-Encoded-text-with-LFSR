 # Image steganography method using Huffman Encoded Text with LFSR

## `encode(num_pieces=[int], message=[str], img=[str])`
* Use `encode()` to encode a message into a png image
* `num_pieces` -> number of sections that the image will be split into. Must be a square integer
* `message` -> message to be encoded. Can only contain alphabet, space and "."
* `img` -> filename of the cover image. Must be a png

* Returns -> private key as an array to use in decode method
        
## `decode(private_key=[array-like], img=[str])`
* Use `decode()` to decode the message out of a stego image created with `encode()`
* `private-key` -> array-like object representing the private key used during encoding. Composed of  "[ num_pieces, LSFR.seed, LSFR.tapped, key.freqs.value() ]"
* `img` -> filename of the stego image. Must be a png

 
