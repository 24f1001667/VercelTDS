from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import List
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"],
)

class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

class RegionMetrics(BaseModel):
    region: str
    avg_latency: float
    p95_latency: float
    avg_uptime: float
    breaches: int

class TelemetryResponse(BaseModel):
    regions: List[RegionMetrics]

def load_telemetry_data():
    possible_paths = [
        'api/telemetry.json',
        'telemetry.json',
        os.path.join(os.getcwd(), 'api/telemetry.json'),
        os.path.join(os.path.dirname(__file__), 'telemetry.json')
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
        except Exception as e:
            continue
    
    raise FileNotFoundError("telemetry.json not found")

# Add GET endpoint for health check
@app.get("/")
def read_root():
    return {
        "service": "eShopCo Latency Monitor",
        "status": "online",
        "endpoints": {
            "POST /": "Submit telemetry analysis request"
        }
    }

# POST endpoint for telemetry analysis
@app.post("/", response_model=TelemetryResponse)
def analyze_telemetry(request: TelemetryRequest):
    try:
        df = load_telemetry_data()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    df_filtered = df[df['region'].isin(request.regions)]
    
    metrics = []
    for region in request.regions:
        region_data = df_filtered[df_filtered['region'] == region]
        
        if region_data.empty:
            continue
        
        avg_latency = region_data['latency_ms'].mean()
        p95_latency = region_data['latency_ms'].quantile(0.95)
        avg_uptime = region_data['uptime_pct'].mean()
        breaches = len(region_data[region_data['latency_ms'] > request.threshold_ms])
        
        metrics.append(RegionMetrics(
            region=region,
            avg_latency=round(avg_latency, 2),
            p95_latency=round(p95_latency, 2),
            avg_uptime=round(avg_uptime, 4),
            breaches=breaches
        ))
    
    return {"regions": metrics}
