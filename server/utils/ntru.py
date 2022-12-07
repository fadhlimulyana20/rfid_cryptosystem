from ntru.ntrucipher import NtruCipher

if __name__ == "__main__":
    ntru = NtruCipher(251, 3, 128)
    ntru.generate_random_keys()
    print(ntru.g_poly, ntru.f_poly, ntru.R_poly)