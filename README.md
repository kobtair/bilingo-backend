# Bilingo‑Backend Setup & Run

Backend technology stack: **Python 3.10+**, **Flask**, **MongoDB**, **python-dotenv**.

---

## 1. Clone & Setup Virtual Environment

```bash
git clone https://github.com/kobtair/bilingo-backend.git
cd bilingo-backend
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Environment Variables

Create a file named `.env` in the root directory:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority&appName=<app-name>
JWT_SECRET=<your-jwt-secret>
PORT=3000
NODE_ENV=development
CORS_ORIGIN=http://localhost:3000
LOG_LEVEL=info
OPENAI_API=<your-openai-api-key>
```

---

## 4. Run the Flask App

```bash
export FLASK_APP=app.py
flask run --port 5000
```

The server will be live at `http://127.0.0.1:5000`.

---

## 5. Optional: Docker

```bash
docker build -t bilingo-backend .
docker run -e MONGODB_URI=... -p 5000:5000 bilingo-backend
```