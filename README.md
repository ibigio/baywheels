# BayWheels Playground
Playing around with BayWheels (LyftBikes) API and other endpoints I found. Also a tiny library for making super-fast batches of async HTTP requests. *NOTE: This is very much an incomplete, unpolished repo that I pushed just for safekeeping and sharing.*

## Files

### `baywheels.py`: BayWheels Client
Basic Python client for the BayWheels API (documented and otherwise).

### `fast_requests.py`: Fast Requests Library
Tiny library for making super-fast batches of requets.

### `final.py`
Don't mind this file... Just playing around with the API and may have found something fun.

## Running
Both `baywheels.py` and `final.py` expect some environment variables to be set. To set them, I just created a `secrets.sh` file with the following format:
```bash
export AUTH_TOKEN="..."
export API_KEY="..."
export MEMBER_ID="..."

```
Before running the python code, I set them like so:
```bash
source secrets.sh
```
