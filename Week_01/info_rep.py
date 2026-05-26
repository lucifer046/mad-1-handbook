# Demonstrating Encoding in Python

text = "Hello Ñ" # English + Spanish character

# ASCII Encoding
try:
    print(f"ASCII: {text.encode('ascii')}")
except UnicodeEncodeError as e:
    print(f"ASCII Error: {e} (ASCII cannot handle 'Ñ')")

# UTF-8 Encoding (Web Standard)
utf8_encoded = text.encode('utf-8')
print(f"UTF-8: {utf8_encoded}")
print(f"UTF-8 Hex: {utf8_encoded.hex()}")

# UTF-16 Encoding
utf16_encoded = text.encode('utf-16')
print(f"UTF-16: {utf16_encoded}")

# UTF-32 Encoding
utf32_encoded = text.encode('utf-32')
print(f"UTF-32: {utf32_encoded}")

# Decoding back to string
print(f"Decoded: {utf8_encoded.decode('utf-8')}")

# Byte values
print("\nByte values for 'Ñ' in UTF-8:")
char_n = "Ñ"
encoded_n = char_n.encode('utf-8')
for b in encoded_n:
    print(f"Decimal: {b} | Binary: {bin(b)}")
