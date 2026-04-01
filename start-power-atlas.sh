#!/bin/bash
# Kill any existing instances on these ports
lsof -ti:8099 | xargs kill -9 2>/dev/null
lsof -ti:8098 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null

python3 "/Users/rchairez/Documents/Apps/DC POWER PROJECTS/VO201 Power Project/netbox-proxy.py" &
python3 "/Users/rchairez/Documents/Apps/DC POWER PROJECTS/VO201 Power Project/jira-proxy.py" &

echo "NetBox proxy running on port 8099"
echo "Jira proxy running on port 8098"
echo "Starting HTTP server on http://localhost:8080/VO201-power-distribution.html"

cd "/Users/rchairez/Documents/Apps/DC POWER PROJECTS/VO201 Power Project" && python3 -m http.server 8080
