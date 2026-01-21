# 🔐 Password Hash Playground

**Multi-language (UZ / EN) responsive web app** for learning and testing different password hashing algorithms.  
Built with **Flask**, **Argon2**, **Bcrypt**, **Passlib**, and deployable with **Docker**.

---

## 🧩 Features

- ✅ Multi-language support (Uzbek / English)  
- ✅ Responsive design (mobile, tablet, desktop)  
- ✅ Supports multiple hashers:
  - Argon2id
  - Bcrypt
  - Scrypt
  - PBKDF2-SHA256 / SHA512
  - SHA512-crypt
  - MD5-crypt
  - NTLM
  - LDAP SSHA
  - MD5
- ✅ Detailed hasher info:
  - Name, Year, Author
  - Standard, Purpose
  - When to use / Not to use
  - Security & Status
- ✅ Password validation (8–32 characters)  
- ✅ Hash analytics (hash time in ms)  
- ✅ Production-ready Flask app with `debug=False`  
- ✅ Docker & Docker Compose ready

---

## ⚙️ Installation

### Requirements

- Python 3.12+  
- Docker (optional, for containerized deployment)  

---

### 1️⃣ Clone repository

```bash
git clone https://github.com/asadback25/password-hashers.git
cd password-hash-playground
```

### 2️⃣ Install dependencies (local Python)

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Flask locally

```bash
export FLASK_APP=app.py
export FLASK_ENV=production
flask run --host=0.0.0.0
```

Open browser at: [http://localhost:5000](http://localhost:5000)

---

### 4️⃣ Run with Docker

#### Build & Run

```bash
docker compose up --build
```

or (if using Docker Compose v1)

```bash
docker-compose up --build
```

Open browser at: [http://localhost:5000](http://localhost:5000)

---

## 🖥️ Project Structure

```
password-hash-playground/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main HTML template
└── static/
    └── style.css           # Responsive CSS
├── Dockerfile              # Docker build
└── docker-compose.yml      # Docker Compose config
```

---

## 🌐 Languages

- Uzbek 🇺🇿
- English 🇬🇧  
Switch languages via links on header:  

```text
?lang=uz  |  ?lang=en
```

---

## 🔐 Supported Hashers

| Hasher        | Year | Security | Status       |
|---------------|------|----------|-------------|
| Argon2id      | 2015 | Very Strong | Recommended |
| Bcrypt        | 1999 | Strong      | Recommended |
| Scrypt        | 2009 | Strong      | Recommended |
| PBKDF2-SHA256 | 2000 | Good        | Acceptable  |
| PBKDF2-SHA512 | 2000 | Good        | Acceptable  |
| SHA512-crypt  | 2008 | Medium      | Legacy      |
| MD5-crypt     | 1994 | Weak        | Legacy      |
| NTLM          | 1993 | Broken      | Broken      |
| LDAP SSHA     | 1999 | Weak        | Legacy      |
| MD5           | 1992 | Broken      | Broken      |

---

## 🖌️ Frontend

- Responsive cards for:
  - Password input & hasher selection  
  - Hashed password output  
  - Analytics (hash time)  
  - Hasher info (metadata)  
- Color-coded:
  - ✅ Success / recommended (green)  
  - ⚠️ Weak / legacy (yellow)  
  - ❌ Broken (red)  

---

## ⚡ Production Recommendations

1. Use **Gunicorn** for production-grade Flask server:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. Optionally, add **Nginx** as reverse proxy with HTTPS.  
3. Use `.env` for sensitive configs (`SECRET_KEY`, etc.)  
4. Persist data / logs via Docker volumes if needed.

---

## 🔗 References

- [Flask Documentation](https://flask.palletsprojects.com/)  
- [Argon2 Password Hashing](https://www.cryptolux.org/index.php/Argon2)  
- [Passlib Hashing Library](https://passlib.readthedocs.io/)  
- [Docker Documentation](https://docs.docker.com/)  

---



MIT License
