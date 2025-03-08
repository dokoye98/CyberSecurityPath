import hashlib

inputFile = 'PlaintextPasswords.txt'
outputFile = 'MD5Hashes.txt'

with open(inputFile, "r", encoding="utf-8", errors="ignore") as infile, open(outputFile, "w") as outfile:
    for line in infile:
        password = line.strip()
        hash_value = hashlib.md5(password.encode()).hexdigest()
        outfile.write(f"{password}:{hash_value}\n")

print(f"MD5 hashes saved to {outputFile}")