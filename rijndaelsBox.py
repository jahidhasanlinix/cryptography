from typing import List

def multiply_ints_as_polynomials(x: int, y: int) -> int:
    z = 0
    while x:
        if x & 1:
            z ^= y
        y <<= 1
        x >>= 1
    return z

def number_bits(x: int) -> int:
    return x.bit_length()

def mod_int_as_polynomial(x: int, m: int) -> int:
    nbm = number_bits(m)
    while True:
        nbx = number_bits(x)
        if nbx < nbm:
            return x
        mshift = m << (nbx - nbm)
        x ^= mshift

def rijndael_multiplication(x: int, y: int) -> int:
    z = multiply_ints_as_polynomials(x, y)
    m = 0b100011011
    return mod_int_as_polynomial(z, m)

def rijndael_inverse(x: int) -> int:
    return next((y for y in range(256) if rijndael_multiplication(x, y) == 1), 0)

def dot_product(x: int, y: int) -> int:
    return bin(x & y).count('1') % 2

def affine_transformation(A: int, x: int, b: int) -> int:
    y = sum((dot_product((A >> (8 * i)) & 0xff, x) << i) for i in range(8))
    return y ^ b

def rijndael_sbox(x: int) -> int:
    xinv = rijndael_inverse(x)
    A = 0xf1f1f1f1f0f0f0f0
    b = 0x63
    return affine_transformation(A, xinv, b)

def generate_rijndael_sbox() -> List[int]:
    return [rijndael_sbox(x) for x in range(256)]

def print_rijndael_sbox(sbox: List[int]) -> None:
    for row in range(16):
        print(' '.join(f'{sbox[16*row + col]:02x}' for col in range(16)))

if __name__ == "__main__":
    sbox = generate_rijndael_sbox()
    print_rijndael_sbox(sbox)