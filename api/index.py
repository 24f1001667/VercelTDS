from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: int

# Paste your JSON data here as a Python list
DATA = [
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 106.72,
    "uptime_pct": 99.089,
    "timestamp": 20250301
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 217.1,
    "uptime_pct": 97.746,
    "timestamp": 20250302
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 192.11,
    "uptime_pct": 97.77,
    "timestamp": 20250303
  },
  {
    "region": "apac",
    "service": "payments",
    "latency_ms": 192.04,
    "uptime_pct": 99.244,
    "timestamp": 20250304
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 151.53,
    "uptime_pct": 98.627,
    "timestamp": 20250305
  },
  {
    "region": "apac",
    "service": "support",
    "latency_ms": 204.58,
    "uptime_pct": 99.159,
    "timestamp": 20250306
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 175.77,
    "uptime_pct": 98.185,
    "timestamp": 20250307
  },
  {
    "region": "apac",
    "service": "recommendations",
    "latency_ms": 225.79,
    "uptime_pct": 97.227,
    "timestamp": 20250308
  },
  {
    "region": "apac",
    "service": "checkout",
    "latency_ms": 173.5,
    "uptime_pct": 97.236,
    "timestamp": 20250309
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 140.91,
    "uptime_pct": 98.456,
    "timestamp": 20250310
  },
  {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 196.3,
    "uptime_pct": 97.818,
    "timestamp": 20250311
  },
  {
    "region": "apac",
    "service": "analytics",
    "latency_ms": 151.61,
    "uptime_pct": 97.366,
    "timestamp": 20250312
  },
  {
    "region": "emea",
    "service": "analytics",
    "latency_ms": 142.97,
    "uptime_pct": 99.034,
    "timestamp": 20250301
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 168.79,
    "uptime_pct": 98.916,
    "timestamp": 20250302
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 101.37,
    "uptime_pct": 98.763,
    "timestamp": 20250303
  },
  {
    "region": "emea",
    "service": "catalog",
    "latency_ms": 115.61,
    "uptime_pct": 97.457,
    "timestamp": 20250304
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 184.27,
    "uptime_pct": 97.869,
    "timestamp": 20250305
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 169.61,
    "uptime_pct": 97.352,
    "timestamp": 20250306
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 190.41,
    "uptime_pct": 97.616,
    "timestamp": 20250307
  },
  {
    "region": "emea",
    "service": "payments",
    "latency_ms": 158.65,
    "uptime_pct": 97.595,
    "timestamp": 20250308
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 211.23,
    "uptime_pct": 98.265,
    "timestamp": 20250309
  },
  {
    "region": "emea",
    "service": "support",
    "latency_ms": 163.71,
    "uptime_pct": 97.643,
    "timestamp": 20250310
  },
  {
    "region": "emea",
    "service": "recommendations",
    "latency_ms": 128.79,
    "uptime_pct": 99.021,
    "timestamp": 20250311
  },
  {
    "region": "emea",
    "service": "checkout",
    "latency_ms": 111.96,
    "uptime_pct": 98.285,
    "timestamp": 20250312
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 186.6,
    "uptime_pct": 97.442,
    "timestamp": 20250301
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 197.52,
    "uptime_pct": 97.57,
    "timestamp": 20250302
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 158.34,
    "uptime_pct": 99.236,
    "timestamp": 20250303
  },
  {
    "region": "amer",
    "service": "payments",
    "latency_ms": 191.76,
    "uptime_pct": 98.007,
    "timestamp": 20250304
  },
  {
    "region": "amer",
    "service": "checkout",
    "latency_ms": 176.54,
    "uptime_pct": 97.942,
    "timestamp": 20250305
  },
  {
    "region": "amer",
    "service": "catalog",
    "latency_ms": 158.56,
    "uptime_pct": 98.47,
    "timestamp": 20250306
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 98.53,
    "uptime_pct": 98.752,
    "timestamp": 20250307
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 153.27,
    "uptime_pct": 97.514,
    "timestamp": 20250308
  },
  {
    "region": "amer",
    "service": "recommendations",
    "latency_ms": 168.06,
    "uptime_pct": 98.951,
    "timestamp": 20250309
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 130.82,
    "uptime_pct": 98.1,
    "timestamp": 20250310
  },
  {
    "region": "amer",
    "service": "support",
    "latency_ms": 161.32,
    "uptime_pct": 98.403,
    "timestamp": 20250311
  },
  {
    "region": "amer",
    "service": "analytics",
    "latency_ms": 214.81,
    "uptime_pct": 97.273,
    "timestamp": 20250312
  }
]

@app.post("/")
def analyze_latency(request: AnalyticsRequest):
    results = {}
    
    for region in request.regions:
        region_data = [record for record in DATA if record["region"] == region]
        
        if not region_data:
            continue
            
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime"] for r in region_data]
        
        avg_latency = sum(latencies) / len(latencies)
        
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index]
        
        avg_uptime = sum(uptimes) / len(uptimes)
        
        breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
        
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return results

