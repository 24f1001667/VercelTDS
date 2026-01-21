from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import List

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Request model
class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

# Response models
class RegionMetrics(BaseModel):
    region: str
    avg_latency: float
    p95_latency: float
    avg_uptime: float
    breaches: int

class TelemetryResponse(BaseModel):
    metrics: List[RegionMetrics]

# Load telemetry data (you'll need to upload this file)
# Place telemetry.csv in the api/ folder
def load_telemetry_data():
    try:
        df = pd.read_csv('api/telemetry.csv')
        return df
    except FileNotFoundError:
        # Return empty DataFrame if file doesn't exist
        return pd.DataFrame()

@app.post("/", response_model=TelemetryResponse)
def analyze_telemetry(request: TelemetryRequest):
    df = load_telemetry_data()
    
    if df.empty:
        return {"metrics": []}
    
    # Filter for requested regions
    df_filtered = df[df['region'].isin(request.regions)]
    
    metrics = []
    for region in request.regions:
        region_data = df_filtered[df_filtered['region'] == region]
        
        if region_data.empty:
            continue
        
        # Calculate metrics
        avg_latency = region_data['latency_ms'].mean()
        p95_latency = region_data['latency_ms'].quantile(0.95)
        avg_uptime = region_data['uptime'].mean()
        breaches = len(region_data[region_data['latency_ms'] > request.threshold_ms])
        
        metrics.append(RegionMetrics(
            region=region,
            avg_latency=round(avg_latency, 2),
            p95_latency=round(p95_latency, 2),
            avg_uptime=round(avg_uptime, 4),
            breaches=breaches
        ))
    
    return {"metrics": metrics}
