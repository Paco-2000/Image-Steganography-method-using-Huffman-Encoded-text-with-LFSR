from key_setup import Key

# Class encodes message into Huffman tree
# Accepts all letters, " " and ".". Message
# needs to end with "!" as an end of text
# marker. Will automatically add it if not 
# included 
class Message:
    def __init__(self, plaintext, key):
        self.plaintext = plaintext
        self.key = key
        self.ciphertext = ''
        if '!' in self.plaintext and self.plaintext[-1] != '!':
            raise ValueError("Error: Character '!' not allowed unless as end of text marker")
        if self.plaintext[-1] != '!':
            self.plaintext += '!'
        for ch in self.plaintext.lower():
            if ch in "abcdefghijklmnopqrstuvwxyz. !":
                self.ciphertext += self.key.values[ch]
            else: 
                raise ValueError('Error: Character {} not allowed'.format(ch))
        


