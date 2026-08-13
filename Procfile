web: uvicorn main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*' --loop uvloop --ws websockets --timeout-keep-alive 120 --limit-concurrency 1000
