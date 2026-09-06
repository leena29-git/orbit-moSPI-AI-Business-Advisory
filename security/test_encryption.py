from app.security.encryption import encrypt_field, decrypt_field

original = "50000"
encrypted = encrypt_field(original)
decrypted = decrypt_field(encrypted)

print("Original :", original)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
assert decrypted == original, "Round-trip failed!"
print("✅ Encryption round-trip works")