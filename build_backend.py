import os
import sys

BASE_DIR = r"C:\Users\Master_Manu\.gemini\antigravity\scratch\codementor-ai\backend"
APP_DIR = os.path.join(BASE_DIR, "app")

def write_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# 1. requirements.txt
write_file("requirements.txt", """fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
pymongo>=4.9.0
google-genai>=1.0.0
pyjwt>=2.8.0
bcrypt>=4.1.2
python-dotenv>=1.0.1
python-multipart>=0.0.9
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
""")

# 2. .env.example
write_file(".env.example", """GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.7-flash
MONGODB_URI=
MONGODB_DB_NAME=codementor_db
JWT_SECRET=super_secret_codementor_jwt_key_2026_change_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
JUDGE0_API_URL=
JUDGE0_API_KEY=
""")

# 3. .env (local default for testing)
write_file(".env", """GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.7-flash
MONGODB_URI=
MONGODB_DB_NAME=codementor_db
JWT_SECRET=super_secret_codementor_jwt_key_2026_change_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
JUDGE0_API_URL=
JUDGE0_API_KEY=
""")

print("Init files written successfully.")
