from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
import os

app = FastAPI()

# Enable CORS - CRITICAL: Must allow OPTIONS for preflight
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Must include OPTIONS
    allow_headers=["*"],
)

class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

class RegionMetrics(BaseModel):
    region: str
    avg_latency: float
    p95_latency: float
    avg_uptime: float
    breaches: int

class TelemetryResponse(BaseModel):
    metrics: List[RegionMetrics]

# Load telemetry data
csv_path = os.path.join(os.path.dirname(__file__), '..', 'telemetry.csv')
df = pd.read_csv(csv_path)

@app.post("/api/telemetry", response_model=TelemetryResponse)
async def analyze_telemetry(request: TelemetryRequest):
    """
    Analyze telemetry data for specified regions.
    """
    metrics = []
    
    for region in request.regions:
        region_data = df[df['region'] == region]
        
        if len(region_data) == 0:
            continue
        
        avg_latency = round(region_data['latency_ms'].mean(), 2)
        p95_latency = round(region_data['latency_ms'].quantile(0.95), 2)
        avg_uptime = round(region_data['uptime_pct'].mean(), 2)
        breaches = int((region_data['latency_ms'] > request.threshold_ms).sum())
        
        metrics.append(RegionMetrics(
            region=region,
            avg_latency=avg_latency,
            p95_latency=p95_latency,
            avg_uptime=avg_uptime,
            breaches=breaches
        ))
    
    return TelemetryResponse(metrics=metrics)

# Explicit OPTIONS handler for preflight
@app.options("/api/telemetry")
async def options_telemetry():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/")
async def read_root():
    return {"status": "ok", "message": "eShopCo Telemetry API"}
