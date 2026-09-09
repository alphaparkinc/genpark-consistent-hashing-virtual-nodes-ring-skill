"""MCP Server for Consistent Hashing Ring Skill."""
import json
import sys
from client import ConsistentHashRing

def main():
    ring = ConsistentHashRing()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "lookup_node",
                            "description": "Route key to server using consistent hashing",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "nodes": {"type": "array", "items": {"type": "string"}},
                                    "key": {"type": "string"}
                                },
                                "required": ["nodes", "key"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                r = ConsistentHashRing()
                for n in args["nodes"]:
                    r.add_node(n)
                srv = r.get_node(args["key"])
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps({"target_node": srv})}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
