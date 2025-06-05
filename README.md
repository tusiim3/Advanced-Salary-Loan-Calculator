# Salary Advance Calculator

A web application for calculating salary advances and loan repayments with compound interest calculations.

## 🏗️ Architecture

- **Frontend**: Streamlit - Interactive UI for user inputs and results display
- **Backend**: FastAPI - RESTful API for calculations and business logic
- **Data Processing**: Pandas - Financial calculations and data manipulation
- **Deployment**: Docker & Docker Compose - Containerized multi-service deployment

## ✨ Features

### Core Functionality
- **Salary Advance Calculator**: Determine eligibility and maximum advance amounts
- **Loan Calculator**: Compound interest calculations with repayment schedules
- **Fee Modeling**: Optional fee calculations for advances
- **Amortization Schedules**: Detailed payment breakdowns using Pandas

### User Interface
- Clean, intuitive Streamlit interface
- Real-time calculation results
- Comprehensive error handling
- Input validation and formatting

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd salary-advance-calculator
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and Run**
   ```bash
   docker compose up --build
   ```

4. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📊 API Endpoints

### POST /calculate_advance
Calculate salary advance eligibility and amounts.

**Request:**
```json
{
  "gross_salary": 50000,
  "pay_frequency": "monthly",
  "requested_advance": 10000
}
```

**Response:**
```json
{
  "eligible": true,
  "max_advance": 15000,
  "approved_amount": 10000,
  "fees": 500,
  "repayment_amount": 10500
}
```

### POST /calculate_loan
Calculate loan repayments with compound interest.

**Request:**
```json
{
  "loan_amount": 100000,
  "interest_rate": 5.5,
  "loan_term_months": 24
}
```

**Response:**
```json
{
  "total_repayment": 105683.32,
  "monthly_payment": 4403.47,
  "total_interest": 5683.32,
  "amortization_schedule": [...]
}
```

## 🔧 Development

### Local Development (Without Docker)

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py --server.port 8501
   ```

### Project Structure
```
salary-advance-calculator/
├── frontend/
│   ├── app.py                 # Complete Streamlit application
│   ├── requirements.txt
│   └── Dockerfile
├── backend/
│   ├── main.py               # Complete FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 💡 Calculation Logic

### Advance Eligibility
- Minimum salary requirements
- Maximum advance limits (percentage of salary)
- Frequency-based calculations using Pandas

### Compound Interest
- Standard compound interest formula
- Pandas DataFrames for amortization schedules
- Configurable compounding periods

### Fee Structure
- Percentage-based fees
- Fixed processing fees
- Transparent fee breakdown

## 🔒 Configuration

### Environment Variables
```env
# API Configuration
BACKEND_URL=http://localhost:8000
FRONTEND_PORT=8501
BACKEND_PORT=8000

# Calculation Parameters
MIN_SALARY=20000
MAX_ADVANCE_PERCENTAGE=30
DEFAULT_INTEREST_RATE=5.5
```

## 🛠️ Technical Assumptions

- **Salary Input**: Gross salary in local currency
- **Pay Frequency**: Monthly, bi-weekly, weekly supported
- **Interest Calculation**: Compound interest, monthly compounding
- **Advance Limits**: 30% of monthly gross salary maximum
- **Loan Terms**: 1-60 months supported

## 🔍 Error Handling

- **Network Failures**: Graceful degradation with user feedback
- **Invalid Inputs**: Comprehensive validation with clear messages
- **Calculation Errors**: Fallback logic and error logging
- **Service Unavailability**: Retry mechanisms and status indicators

## 📈 Deployed Application

**Live URL**: [Your deployed application URL]

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'feat: add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

---

**Note**: This application is for educational purposes. Consult financial professionals for real-world lending decisions.