# pwd-guard-man


**Defensive password strength classifier** for audits and education.


> Ethics & Usage
> - Defensive and educational use only.
> - Do **not** deploy any public endpoint that accepts plaintext passwords.
> - Prefer **client-side** evaluation (see Export section).
> - Obtain explicit consent before evaluating real user passwords. Do not log inputs.
>


## Quickstart


```bash
python -m venv venv && source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
python data/generate_synthetic.py # writes data/synthetic_passwords.jsonl
python -m src.train --train data/synthetic_passwords.jsonl \
--val data/synthetic_passwords.jsonl \
--out model.pt
uvicorn src.server:app --reload
# POST http://127.0.0.1:8000/eval with {"password":"yourpwd"}
```
