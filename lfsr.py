class LFSR:
    # Params:
    #   register : bit array
    #   tapped : array of tapped positions. Integer values
    def __init__(self, register, tapped):
        self.register = register
        self.tapped = tapped
        
        #check if tapped elements are "legal" (within range of register)
        for i in self.tapped:
            if(i > len(self.register) - 1):
                raise ValueError('Tapped position {} outside of range for {}'.format(i, self.register))
    
    # Computes 1 shift of the LFSR. Adds all tapped
    # elements of register (mod 2), appends it to 
    # the end of the register and pops the first 
    # element.
    def shift(self):
        output = 0
        for i in self.tapped:
            output += self.register[i]
        
        output = output % 2
        self.register.append(output)
        return self.register.pop(0)