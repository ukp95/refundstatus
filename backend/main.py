from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional
import io

app = FastAPI(title="SabPaisa Refund Dashboard API")

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to ["http://localhost:5500"] if you use Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded data and audit log
uploaded_data = pd.DataFrame()
audit_log = []

@app.post("/upload-excel/")
def upload_excel(file: UploadFile = File(...)):
    """
    Upload and parse Excel file. Store in memory for search/validation.
    Accepts large files by reading in chunks.
    """
    try:
        # Read file in chunks to handle large files
        contents = b""
        for chunk in iter(lambda: file.file.read(1024 * 1024), b""):
            contents += chunk
        # Read Excel, force all columns as string to preserve leading zeros
        df = pd.read_excel(io.BytesIO(contents), dtype=str)
        # Standardize column names to match expected keys and handle variations
        col_map = {
            'IFSC_Code': 'IFSC',
            'CBS_Account_No': 'Account_No',
            'Refund Amount': 'Refund_Amount',
            'Amount_to_Pay': 'Amount_to_Pay',
            'clienttransId': 'clienttransId',
            'spTransId': 'spTransId',
            'transStatus': 'transStatus',
            'transPaymode': 'transPaymode',
            'Division Name': 'Division_Name',
            'NIT_No': 'NIT_No',
            'Item_No': 'Item_No',
            'Name_of_Bank': 'Name_of_Bank',
            'Branch_Name': 'Branch_Name',
            'Bidding_Firm_Name': 'Bidding_Firm_Name'
        }
        # Remove spaces and unify column names
        df.columns = [col_map.get(c.strip().replace(' ', '_'), c.strip().replace(' ', '_')) for c in df.columns]
        global uploaded_data
        uploaded_data = df
        # Return columns for debugging
        return {"status": "success", "rows": len(df), "columns": list(df.columns)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/search/")
def search_transactions(
    spTransId: Optional[str] = None,
    clienttransId: Optional[str] = None,  # Added for frontend compatibility
    Bidding_Firm_Name: Optional[str] = None,
    NIT_No: Optional[str] = None
):
    """
    Search transactions by filters. Supports Transaction ID, clienttransId (or NIT_No), and Bidding Firm Name.
    Accepts either 'clienttransId' or 'NIT_No' as query param for client transaction ID.
    """
    if uploaded_data.empty:
        raise HTTPException(status_code=404, detail="No data uploaded.")
    df = uploaded_data
    # Filter by Transaction ID
    if spTransId:
        if 'spTransId' in df.columns:
            df = df[df['spTransId'].astype(str).str.contains(str(spTransId), na=False)]
    # Filter by Bidding Firm Name
    if Bidding_Firm_Name:
        if 'Bidding_Firm_Name' in df.columns:
            df = df[df['Bidding_Firm_Name'].astype(str).str.contains(str(Bidding_Firm_Name), na=False)]
    # Filter by clienttransId or NIT_No (whichever is provided)
    client_id_value = clienttransId or NIT_No
    if client_id_value:
        # Try both possible column names for client transaction ID
        if 'clienttransId' in df.columns:
            df = df[df['clienttransId'].astype(str).str.contains(str(client_id_value), na=False)]
        elif 'NIT_No' in df.columns:
            df = df[df['NIT_No'].astype(str).str.contains(str(client_id_value), na=False)]
    return df.to_dict(orient="records")

@app.get("/validate/")
def validate_transactions():
    """
    Auto-validate IFSC, account number, duplicates, eligibility.
    """
    if uploaded_data.empty:
        raise HTTPException(status_code=404, detail="No data uploaded.")
    df = uploaded_data.copy()
    results = []
    seen = set()
    for idx, row in df.iterrows():
        issues = []
        # IFSC validation (handle IFSC or IFSC_Code)
        ifsc = row.get('IFSC') or row.get('IFSC_Code')
        if not isinstance(ifsc, str) or len(ifsc) != 11:
            issues.append('Invalid IFSC')
        # Account number length (handle Account_No or CBS_Account_No)
        acc_no = row.get('Account_No') or row.get('CBS_Account_No')
        if not isinstance(acc_no, str) or not (9 <= len(acc_no) <= 18):
            issues.append('Invalid Account Number')
        # Duplicate check
        key = (row.get('spTransId'), acc_no)
        if key in seen:
            issues.append('Duplicate Transaction')
        else:
            seen.add(key)
        # Eligibility (example: NIT_No must not be empty)
        if not row.get('NIT_No'):
            issues.append('Missing NIT_No')
        results.append({"spTransId": row.get('spTransId'), "issues": issues})
    return results

@app.post("/trigger-refund/")
def trigger_refund(spTransId: str):
    """
    Trigger refund for a transaction (mock implementation).
    """
    # In real scenario, call refund API here
    audit_log.append({"spTransId": spTransId, "action": "refund_triggered"})
    return {"status": "refund triggered", "spTransId": spTransId}

@app.get("/audit-log/")
def get_audit_log():
    """
    Get audit log of refund actions.
    """
    return audit_log

@app.get("/metrics/")
def get_metrics():
    """
    Return metrics for dashboard visualizations.
    """
    if uploaded_data.empty:
        return {"total": 0, "pending": 0, "failures": 0}
    total = len(uploaded_data)
    # For demo, count rows with issues as failures
    validation = validate_transactions()
    failures = sum(1 for r in validation if r['issues'])
    pending = total - failures
    return {"total": total, "pending": pending, "failures": failures}
