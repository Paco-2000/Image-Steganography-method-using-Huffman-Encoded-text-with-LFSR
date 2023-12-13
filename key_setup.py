import random
import heapq
from lfsr import LFSR

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.right = right
        self.left = left
        self.huff = ''

    def __lt__(self, nxt):
        return self.freq < nxt.freq

class Key:
    def __init__(self, num_pieces, register=[], tapped=[], dic_values=[]):
        self.freqs = set_frequencies(dic_values)
        self.root = tree_build_up(self.freqs)
        if tapped and register:
            self.lfsr = LFSR(register, tapped)
        else:
            self.lfsr = generate_lfsr()
        self.seed = self.lfsr.register.copy()
        self.values = {}
        self.num_pieces = num_pieces
        tree_to_dic(self.root, self.values)
    
    # utility function to print huffman 
    # codes for all symbols in the newly 
    # created Huffman tree 
    def print_values(self, node=-1, val=''): 
        if(node == -1):
            node = self.root
    
        # huffman code for current node 
        newVal = val + str(node.huff) 
    
        # if node is not an edge node 
        # then traverse inside it 
        if(node.left): 
            Key.print_values(self, node.left, newVal) 
        if(node.right): 
            Key.print_values(self, node.right, newVal) 
    
            # if node is edge node then 
            # display its huffman code 
        if(not node.left and not node.right): 
            print(f"{node.symbol} -> {newVal}")
    
    def get_private_key(self):
        return [self.num_pieces, self.seed, self.lfsr.tapped, list(self.freqs.values())]


# This uses the random library which is not suited for cryptographic 
# purposes. Ideally we would use something more secure to shuffle the
# array like the Fisher-Yates shuffle algorithm. Weights are taken 
# from the 29 highest frequencies appearing in MacBeth
def set_frequencies(vals=[]):
    base_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.', '!']
    freqs  = [15656, 9451, 7164, 6103, 6102, 5346, 5055, 5010, 4687, 4576, 3820, 3397, 3328, 2529, 2509, 2191, 1949, 1702, 1678, 1531, 1483, 1377, 1361, 1015, 707, 648, 529, 243, 201]
    if(len(vals) != 29):
        random.shuffle(freqs)
    else:
        freqs = vals
    freq_dic = {}
    for i in range(len(base_alphabet)):
        freq_dic[base_alphabet[i]] = freqs[i]

    return freq_dic


# Frequencies are calculated based on how many
# times each character appears in MacBeth. 
# This is just to generate some "random" values
# They will be randomly reattributed later
def calculate_frequencies(input_file):
    char_freq = {}
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            for ch in line:
                if(ch.lower() not in char_freq):
                    char_freq[ch.lower()] = 0
                char_freq[ch.lower()] += 1

    f.close()

    # Get the 29 highest weights 
    weights = list(char_freq.values())
    weights.sort()
    weights = weights[::-1]
    weights = weights[:29]

    with open("weights.txt", 'w') as f:
        f.write(str(weights))
        f.close()
    return char_freq



# Buildup a tree based on the frequencies given. 
# Returns root of the tree
def tree_build_up(freq_dic):
    nodes = []

    for x in freq_dic:
        heapq.heappush(nodes, Node(freq_dic[x], x))

    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        left.huff = 0
        right.huff = 1

        newNode = Node(left.freq+right.freq, left.symbol+right.symbol, left, right)

        heapq.heappush(nodes, newNode)

    return nodes[0]

def tree_to_dic(node, dic, val=''):
    # huffman code for current node 
    newVal = val + str(node.huff) 
  
    # if node is not an edge node 
    # then traverse inside it 
    if(node.left): 
        tree_to_dic(node.left, dic, newVal)
    if(node.right): 
        tree_to_dic(node.right, dic, newVal)
  
        # if node is edge node then 
        # add its huffman code to dic
    if(not node.left and not node.right): 
        dic[node.symbol] = newVal

# Method creates LFSR that will have a cycle>=10
# For this, we need a register with len >=4 and 
# at least 1 tapped >= 4. Once again using 
# random library for simplicity sake. Would 
# ideallly use something more robust for cryptography
def generate_lfsr():
    size_register = random.randrange(4, 25) 
    num_tapped = random.randrange(1, size_register) 

    # Generate register
    register = []
    binary = [0, 1]
    for i in range(size_register):
        register.append(random.choice(binary)) # Randomly chose 1 or 0

    # Generate tapped positions, start with 1 position that's >=4,
    # Will end up with at least 2 tapped positions
    tapped = [random.randrange(4, size_register-1)]
    for i in range(num_tapped):
        next = random.randrange(0, size_register - 1)
        if next not in tapped:
            tapped.append(next)

    # Return LFSR object
    return LFSR(register, tapped)


