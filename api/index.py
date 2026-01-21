from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI()

# Enable CORS so any website can call your endpoint
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Define what the incoming request should look like
class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: int

# Load the latency data from your JSON file
with open("q-vercel-latency.json", "r") as f:
    data = json.load(f)

@app.post("/")
def analyze_latency(request: AnalyticsRequest):
    results = {}
    
    for region in request.regions:
        # Filter data for this specific region
        region_data = [record for record in data if record["region"] == region]
        
        if not region_data:
            continue
            
        # Calculate metrics
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime"] for r in region_data]
        
        # Average latency (mean)
        avg_latency = sum(latencies) / len(latencies)
        
        # P95 latency (95th percentile)
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index]
        
        # Average uptime
        avg_uptime = sum(uptimes) / len(uptimes)
        
        # Count breaches (records above threshold)
        breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
        
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return results
