from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], # Update this with your frontend domain in production
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class AdvanceRequest (BaseModel):
    gross_salary: float
    advance_amount: float
    currency: str
    pay_frequency: str

class LoanRequest(BaseModel):
    loan_amount: float
    interest_rate: float
    loan_term: int
    currency: str

advance_eligibility = {
    "UGX": 500000,
    "USD": 200,
    "KES": 20000,
    "TZS": 400000,
    "GBP": 120,
    "EUR": 150,
    "RWF": 200000,
}

FEE_RATE = 0.03

@app.post("/calculate_advance")
def calculate_advance(req: AdvanceRequest):

    if req.currency not in advance_eligibility:
        raise HTTPException(status_code = 400, detail = "Unsupported currency")
    
    eligible = (
        req.gross_salary >= advance_eligibility[req.currency] and
        req.pay_frequency.strip().lower == "month"
    )

    max_advance = 0.5 * req.gross_salary

    if not eligible or req.advance_amount > max_advance:
        return {"eligible": False, "max_advance": round(max_advance, 2)}




