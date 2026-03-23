import json
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen


class JsonHttpClient:
    def request(self, url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> Any:
        data = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        req = Request(url=url, method=method.upper(), headers=headers, data=data)
        with urlopen(req, timeout=15) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
