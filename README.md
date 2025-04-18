# Endpoint Availability Monitor

This is a simple Python script that monitors HTTP endpoints and calculates availability by domain. It's designed with Site Reliability Engineering (SRE) principles in mind — particularly measuring reliability consistently and ensuring future developers can build on top of it.

## Features

- Reads configuration from a YAML file
- Measures availability for each domain, regardless of ports
- Tracks response codes (must be 200–299) and ensures the response time is under 500ms
- Cumulative stats — not per-cycle
- Runs checks every 15 seconds, no matter how many endpoints are defined

---

## How to Run

1. Clone the repo.

2. Make sure you have Python 3 installed:

   ```bash
   python3 main.py sample.yaml