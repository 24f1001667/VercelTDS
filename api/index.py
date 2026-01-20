from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd
import os
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

# Try multiple paths to find the CSV
def load_csv():
    possible_paths = [
        'telemetry.csv',
        '../telemetry.csv',
        './telemetry.csv',
        os.path.join(os.path.dirname(__file__), '..', 'telemetry.csv'),
        os.path.join(os.path.dirname(__file__), 'telemetry.csv'),
        '/var/task/telemetry.csv',
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                return pd.read_csv(path)
        except Exception as e:
            continue
    
    raise FileNotFoundError(f"Could not find telemetry.csv. Searched: {possible_paths}")

try:
    df = load_csv()
except Exception as e:
    print(f"Error loading CSV: {e}", file=sys.stderr)
    df = None

@app.post("/")
async def analyze_telemetry(request: TelemetryRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="CSV file not loaded")
    
    metrics = []
    
    for region in request.regions:
        region_data = df[df['region'] == region]
        
        if len(region_data) == 0:
            continue
        
        avg_latency = round(float(region_data['latency_ms'].mean()), 2)
        p95_latency = round(float(region_data['latency_ms'].quantile(0.95)), 2)
        avg_uptime = round(float(region_data['uptime_pct'].mean()), 2)
        breaches = int((region_data['latency_ms'] > request.threshold_ms).sum())
        
        metrics.append({
            "region": region,
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        })
    
    return {"metrics": metrics}

@app.get("/")
async def health():
    csv_loaded = df is not None
    return {
        "status": "ok" if csv_loaded else "error",
        "csv_loaded": csv_loaded,
        "csv_rows": len(df) if csv_loaded else 0
    }