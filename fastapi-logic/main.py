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




