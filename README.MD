# TinyScanner

## Overview
TinyScanner is a lightweight port scanning tool written in Python. It supports both TCP and UDP scanning with multi-threading capabilities.

## Features
- TCP and UDP port scanning
- Single port or port range scanning
- Multi-threading support (2-100 threads)
- Service name detection
- Real-time scan results

## Usage
```bash
tinyscanner [OPTIONS] [HOST] [PORT]

Options:
    -p, --port PORT    Port or port range (e.g., 80 or 80-83)
    -u, --udp         Enable UDP scanning
    -t, --tcp         Enable TCP scanning
    -n, --threads N   Set number of threads (2-100, optional)
```

## Example Commands
```bash
# Scan a single TCP port
tinyscanner example.com -p 80 -t

# Scan UDP ports range with threads
tinyscanner example.com -p 1-1024 -u -n 50
```

## Output
The scanner displays:
- Real-time scan results for each port
- Service name for each port
- Summary of open ports at completion

## Error Handling
- Invalid ports or ranges
- Network errors
- Host resolution failures
- Graceful interrupt handling

## Requirements
- Python 3.x
- Standard library modules (socket, argparse, concurrent.futures)
