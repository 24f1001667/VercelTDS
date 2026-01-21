from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
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
    metrics: List[RegionMetrics]

# Load telemetry data with proper path handling
def load_telemetry_data():
    # Try multiple path options for Vercel deployment
    possible_paths = [
        'api/telemetry.csv',
        'telemetry.csv',
        os.path.join(os.getcwd(), 'api/telemetry.csv'),
        os.path.join(os.path.dirname(__file__), 'telemetry.csv')
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                df = pd.read_csv(path)
                return df
        except Exception as e:
            continue
    
    raise FileNotFoundError("telemetry.csv not found in any expected location")

@app.get("/debug")
def debug_info():
    """Debug endpoint to check available data"""
    try:
        df = load_telemetry_data()
        return {
            "file_found": True,
            "total_records": len(df),
            "columns": list(df.columns),
            "unique_regions": df['region'].unique().tolist() if 'region' in df.columns else [],
            "sample_data": df.head(3).to_dict('records')
        }
    except Exception as e:
        return {
            "file_found": False,
            "error": str(e),
            "cwd": os.getcwd(),
            "files_in_cwd": os.listdir(os.getcwd()),
            "files_in_api": os.listdir('api') if os.path.exists('api') else []
        }

@app.post("/", response_model=TelemetryResponse)
def analyze_telemetry(request: TelemetryRequest):
    try:
        df = load_telemetry_data()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
