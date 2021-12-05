import random

# simple mutator that flips random bits
class BitFlippingMutator:

    '''
    parameters:
    ratio - proportion of bits that are changing
    '''
    def __init__(self, ratio):
        self.ratio = ratio

    '''
    xor 2 arrays of bytes
    '''
    def _xor(self, a, b):
        return bytes([x^y for x,y in zip(a,b)])

    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        bits_to_flip = int((len(data) * 8) * self.ratio)

        mask = [0] * (len(data)*8)
        for _ in range(bits_to_flip):
            #flip random bit
            mask[random.randint(0,len(mask)-1)] = 1

        # convert mask to bytes
        mask = bytes([int("".join(map(str, mask[i:i+8])), 2) for i in range(0, len(mask), 8)])

        return self._xor(data, mask)


