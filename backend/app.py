
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt, datetime, os
import openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SECRET = "supersecretkey1234567890123456"
openai.api_key = os.getenv("OPENAI_API_KEY")

users = {}

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    users[user.username] = user.password
    return {"msg": "registered"}

@app.post("/login")
def login(user: User):
    if users.get(user.username) == user.password:
        token = jwt.encode(
            {"user": user.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            SECRET,
            algorithm="HS256"
        )
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid")

def verify(token):
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/analyze")
def analyze(data: dict, token: str):
    verify(token)
    value = data.get("value", 0)
    if value > 5:
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Explain anomaly {value}"}]
        )
        return {"status": "Anomaly", "llm": res["choices"][0]["message"]["content"]}
    return {"status": "Normal"}
