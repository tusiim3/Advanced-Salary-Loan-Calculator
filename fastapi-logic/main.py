from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AdvanceRequest(BaseModel):
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
        raise HTTPException(status_code=400, detail="Unsupported currency")

    eligible = (
        req.gross_salary >= advance_eligibility[req.currency]
        and req.pay_frequency.strip().lower() == "month"
    )

    max_advance = 0.5 * req.gross_salary

    if not eligible or req.advance_amount > max_advance:
        return {"eligible": False, "max_advance": round(max_advance, 2)}

    df = pd.DataFrame({"advance_amount": [req.advance_amount], "fee_rate": [FEE_RATE]})
    df["fee"] = df["advance_amount"] * df["fee_rate"]
    df["total_repayable"] = df["advance_amount"] + df["fee"]

    return {
        "eligible": True,
        "fee_rate": FEE_RATE,
        "fee": round(df.loc[0, "fee"], 2),
        "total_repayable": round(df.loc[0, "total_repayable"], 2),
        "max_advance": round(max_advance, 2),
    }


def generate_amortisation_schedule(principal, rate_annual, term_months):
    r = rate_annual / 12 / 100
    if r == 0:
        emi = principal / term_months
    else:
        emi = principal * r * (1 + r) ** term_months / ((1 + r) ** term_months - 1)

        data = []
        balance = principal

        for month in range(1, term_months + 1):
            interest = balance * r
            principal_payment = emi - interest
            balance -= principal_payment

            data.append(
                [
                    month,
                    round(emi, 2),
                    round(principal_payment, 2),
                    round(interest, 2),
                    round(max(balance, 0)),
                    2,
                ]
            )

        df = pd.DataFrame(
            data, columns=["Month", "EMI", "Principal", "Interest", "Balance"]
        )  # , "Total Payment" ])
        return df, emi


@app.post("/calculate_loan")
def calculate_loan(req: LoanRequest):
    df, emi = generate_amortisation_schedule(
        req.loan_amount, req.interest_rate, req.loan_term
    )
    total_repayable = df["EMI"].sum()

    schedule = df.to_dict(orient="records")

    return {
        "emi": round(emi, 2),
        "total_repayable": round(total_repayable, 2),
        "schedule": schedule,
    }
