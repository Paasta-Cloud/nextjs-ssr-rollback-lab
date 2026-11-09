"""Check server-rendered HTML twice at the same URL, without a JavaScript runtime."""
import datetime, html, json, re, sys, urllib.request, uuid

url, expected = sys.argv[1:]
observations = []
for _ in range(2):
    with urllib.request.urlopen(url, timeout=30) as response:
        raw = response.read().decode()
        match = re.search(r'<pre id="sample">(.*?)</pre>', raw, re.S)
        assert response.status == 200 and match, "expected the probe in HTTP 200 HTML"
        data = json.loads(html.unescape(match[1]))
        assert data["release"] == expected and uuid.UUID(data["request"]).version == 4
        when = datetime.datetime.fromisoformat(data["renderedAt"].replace("Z", "+00:00"))
        assert abs((datetime.datetime.now(datetime.timezone.utc)-when).total_seconds()) < 120
        observations.append(data)
assert observations[0]["request"] != observations[1]["request"]
assert observations[0]["renderedAt"] != observations[1]["renderedAt"]
print(json.dumps({"url": url, "observations": observations}, indent=2))
