from app.security.auth import hash_password, verify_password

password = "mysecretpassword"
hashed = hash_password(password)

print("Original:", password)
print("Hashed:", hashed)
print("Verify correct password:", verify_password(password, hashed))
print("Verify wrong password:", verify_password("wrongpass", hashed))