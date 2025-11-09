#!/bin/sh
set -e

echo "=== Entrypoint: attempting to sync system clock ==="

# Try ntpdate first (most common)
if command -v ntpdate >/dev/null 2>&1; then
  echo "-> running ntpdate -u pool.ntp.org"
  ntpdate -u pool.ntp.org || echo "ntpdate failed (non-fatal)"
fi

# Try sntp if present
if command -v sntp >/dev/null 2>&1; then
  echo "-> running sntp -s pool.ntp.org"
  sntp -s pool.ntp.org || echo "sntp failed (non-fatal)"
fi

# Print the UTC time so logs show the synced time (useful for debugging)
echo "Local time (UTC):"
date -u +"%Y-%m-%d %H:%M:%S %Z"

# Small pause to let the system settle (helps on some hosts)
sleep 1

echo "=== Starting application ==="
# Replace with the correct start command if different
exec python /app/run.py