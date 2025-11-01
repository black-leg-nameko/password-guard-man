from fastapi import FastAPI
from pydantic import BaseModel
import torch
import torch.nn.functional as F
from src.model import SmallTransformerClassifier
from src.dataset import encode, CHARS

app = FastAPI()
MODEL_PATH = "model.pt"

class Req(BaseModel):
    password: str

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SmallTransformerClassifier(vocab_size=len(CHARS))
try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
except Exception as e:
    print("model not loaded:", e)
    model = None

def generate_advice(pwd: str, label: int):
    adv = []
    if label == 0:
        adv.append("Too short")
        adv.append("You should use symbols, numbers, uppercases")
    elif label == 1:
        adv.append("You should set password longer than 12 words")
    else:
        adv.append("Your password is safe!")
    return adv

@app.post("/eval")
def eval_pwd(r: Req):
    if model is None:
        return {"error":"model not loaded"}
    ids = torch.tensor([encode(r.password)], dtype=torch.long).to(device)
    with torch.no_grad():
        logits = model(ids)
        probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
        label = int(probs.argmax())
        score = float(probs[label])
    return {"score": score, "label": ["weak","medium","strong"][label], "advice": generate_advice(r.password, label)}
