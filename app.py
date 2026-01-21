from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
from argon2 import PasswordHasher
import bcrypt, hashlib, time

from passlib.hash import sha512_crypt, sha256_crypt, md5_crypt, nthash, ldap_salted_sha1

app = Flask(__name__)
argon2_hasher = PasswordHasher()

# Languages
LANGUAGES = {
    "uz": {
        "password_placeholder": "8–32 belgili password",
        "hasher_select": "Hasher tanlang",
        "hash_btn": "Hashla",
        "error_len": "Password uzunligi 8–32 belgidan iborat bo‘lishi shart",
        "hashed_pass": "Hashlangan password",
        "analytics": "Analytics",
        "hash_time": "Hashlash vaqti",
        "hasher_info": "Hasher haqida",
        "name": "Nomi",
        "year": "Chiqarilgan yil",
        "author": "Muallif",
        "standard": "Standart",
        "purpose": "Maqsadi",
        "when_use": "Qachon ishlatiladi",
        "when_not": "Qachon ishlatilmaydi",
        "security": "Xavfsizlik",
        "status": "Holati"
    },
    "en": {
        "password_placeholder": "Password (8–32 characters)",
        "hasher_select": "Select Hasher",
        "hash_btn": "Hash",
        "error_len": "Password must be between 8 and 32 characters",
        "hashed_pass": "Hashed Password",
        "analytics": "Analytics",
        "hash_time": "Hash Time",
        "hasher_info": "Hasher Info",
        "name": "Name",
        "year": "Year",
        "author": "Author",
        "standard": "Standard",
        "purpose": "Purpose",
        "when_use": "When to use",
        "when_not": "When NOT to use",
        "security": "Security",
        "status": "Status"
    }
}

# High-detail hasher metadata
HASHERS = {

    "argon2": {
        "name": "Argon2id ⭐",
        "year": 2015,
        "author": "Alex Biryukov, Daniel Dinu, Dmitry Khovratovich",
        "standard": "Winner of Password Hashing Competition (PHC)",
        "purpose": "Modern memory-hard password hashing; resistant to GPU/ASIC attacks",
        "when_use": "New production systems requiring strong security and resistance against parallel attacks",
        "when_not": "Very low-resource devices or extremely time-sensitive operations",
        "security": "Very Strong",
        "status": "Recommended",
        "hash": lambda p: argon2_hasher.hash(p)
    },

    "bcrypt": {
        "name": "Bcrypt",
        "year": 1999,
        "author": "Niels Provos & David Mazieres",
        "standard": "OpenBSD",
        "purpose": "Adaptive password hashing with built-in salt; slows brute-force attacks",
        "when_use": "Legacy systems or production applications; still widely supported",
        "when_not": "High parallel GPU attacks may reduce effectiveness if cost factor too low",
        "security": "Strong",
        "status": "Recommended",
        "hash": lambda p: bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
    },

    "scrypt": {
        "name": "Scrypt",
        "year": 2009,
        "author": "Colin Percival",
        "standard": "RFC 7914",
        "purpose": "Memory-hard key derivation function; resistant to large-scale parallel attacks",
        "when_use": "High security password storage in production",
        "when_not": "Low-memory devices or extremely fast requirements",
        "security": "Strong",
        "status": "Recommended",
        "hash": lambda p: generate_password_hash(p, method="scrypt")
    },

    "pbkdf2_sha256": {
        "name": "PBKDF2-SHA256",
        "year": 2000,
        "author": "RSA Labs",
        "standard": "RFC 2898",
        "purpose": "Key derivation function for password storage; adjustable iteration count",
        "when_use": "Compliance-required applications or legacy systems",
        "when_not": "When modern memory-hard functions are preferred",
        "security": "Good",
        "status": "Acceptable",
        "hash": lambda p: generate_password_hash(p, method="pbkdf2:sha256")
    },

    "pbkdf2_sha512": {
        "name": "PBKDF2-SHA512",
        "year": 2000,
        "author": "RSA Labs",
        "standard": "RFC 2898",
        "purpose": "Stronger PBKDF2 variant using SHA512",
        "when_use": "When higher security than SHA256 required",
        "when_not": "Very low CPU environments",
        "security": "Good",
        "status": "Acceptable",
        "hash": lambda p: generate_password_hash(p, method="pbkdf2:sha512")
    },

    "sha512_crypt": {
        "name": "SHA512-crypt",
        "year": 2008,
        "author": "Ulrich Drepper",
        "standard": "Unix crypt",
        "purpose": "Password storage for Unix/Linux systems",
        "when_use": "Legacy Unix/Linux systems",
        "when_not": "Modern web applications; production new apps",
        "security": "Medium",
        "status": "Legacy",
        "hash": lambda p: sha512_crypt.hash(p)
    },

    "md5_crypt": {
        "name": "MD5-crypt ⚠️",
        "year": 1994,
        "author": "Ulrich Drepper",
        "standard": "Unix crypt",
        "purpose": "Legacy Unix password hashing; now insecure",
        "when_use": "Legacy only",
        "when_not": "Any modern password use",
        "security": "Weak",
        "status": "Legacy",
        "hash": lambda p: md5_crypt.hash(p)
    },

    "ntlm": {
        "name": "NTLM ⚠️",
        "year": 1993,
        "author": "Microsoft",
        "standard": "Windows authentication",
        "purpose": "Legacy Windows password hashing",
        "when_use": "Legacy Windows systems",
        "when_not": "Modern secure apps",
        "security": "Broken",
        "status": "Broken",
        "hash": lambda p: nthash.hash(p)
    },

    "ldap_ssha": {
        "name": "LDAP SSHA ⚠️",
        "year": 1999,
        "author": "OpenLDAP Project",
        "standard": "LDAP salted SHA1",
        "purpose": "Salted SHA1 for LDAP directories",
        "when_use": "LDAP legacy systems",
        "when_not": "Modern web applications",
        "security": "Weak",
        "status": "Legacy",
        "hash": lambda p: ldap_salted_sha1.hash(p)
    },

    "md5": {
        "name": "MD5 ❌",
        "year": 1992,
        "author": "Ron Rivest",
        "standard": "RFC 1321",
        "purpose": "Fast hashing, NOT for passwords",
        "when_use": "Checksum or non-password usage",
        "when_not": "Passwords",
        "security": "Broken",
        "status": "Broken",
        "hash": lambda p: hashlib.md5(p.encode()).hexdigest()
    }
}

def validate_password(password: str, lang: str):
    if not (8 <= len(password) <= 32):
        return LANGUAGES[lang]["error_len"]
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "uz")
    if lang not in LANGUAGES:
        lang = "uz"

    error = None
    result = None
    analytics = None
    info = None

    if request.method == "POST":
        password = request.form.get("password", "")
        hasher_key = request.form.get("hasher")

        error = validate_password(password, lang)

        if not error:
            hasher = HASHERS.get(hasher_key)
            if hasher:
                start = time.perf_counter()
                result = hasher["hash"](password)
                analytics = {"time": round((time.perf_counter() - start) * 1000, 3)}
                info = hasher

    return render_template(
        "index.html",
        hashers=HASHERS,
        lang=lang,
        lang_text=LANGUAGES[lang],
        result=result,
        analytics=analytics,
        info=info,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=False)
