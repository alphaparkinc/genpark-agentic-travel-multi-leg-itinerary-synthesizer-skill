"""MCP Server for Agentic Travel Multi-Leg Itinerary Synthesizer."""
import sys
import json
import time
from client import AgenticTravelItinerarySynthesizer

engine = AgenticTravelItinerarySynthesizer()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "synthesize_travel_itinerary":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "synthesize_itinerary")
    if action == "synthesize_itinerary":
        return engine.synthesize_itinerary(
            origin=args.get("origin", "SFO"),
            destination=args.get("destination", "HND"),
            departure_date=args.get("departure_date", "2026-10-15"),
            return_date=args.get("return_date", "2026-10-20"),
            budget_usd=float(args.get("budget_usd", 2500.0)),
            travelers_count=int(args.get("travelers_count", 1)),
            candidate_flights=args.get("candidate_flights"),
            candidate_hotels=args.get("candidate_hotels")
        )
    elif action == "evaluate_layover_risk":
        return engine.evaluate_layover_risk(
            layover_minutes=int(args.get("layover_minutes", 60)),
            is_international=bool(args.get("is_international", False))
        )
    elif action == "calculate_lodging_options":
        return engine.calculate_lodging_options(
            candidate_hotels=args.get("candidate_hotels", [])
        )
    elif action == "compile_booking_manifest":
        itin = engine.synthesize_itinerary(
            origin=args.get("origin", "SFO"),
            destination=args.get("destination", "HND"),
            departure_date=args.get("departure_date", "2026-10-15"),
            return_date=args.get("return_date", "2026-10-20"),
            budget_usd=float(args.get("budget_usd", 2500.0))
        )
        return engine.compile_booking_manifest(itin)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        res = engine.synthesize_itinerary("SFO", "HND", "2026-11-01", "2026-11-06", 2000.0, 1)
        assert res["status"] == "READY_FOR_COMMERCE_HOLD"
        assert res["budget"]["within_budget"] is True
        risk = engine.evaluate_layover_risk(35, is_international=True)
        assert risk["safe_to_book"] is False
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgenticTravelItinerarySynthesizer", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "synthesize_travel_itinerary",
                            "description": "Multi-leg travel synthesis: plan flight segments, evaluate hotel bookings, calculate layover buffer risks, optimize baggage fees, and assemble unified booking manifests.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["synthesize_itinerary", "evaluate_layover_risk", "calculate_lodging_options", "compile_booking_manifest"]},
                                    "origin": {"type": "string"},
                                    "destination": {"type": "string"},
                                    "departure_date": {"type": "string"},
                                    "return_date": {"type": "string"},
                                    "budget_usd": {"type": "number"},
                                    "travelers_count": {"type": "integer"},
                                    "candidate_flights": {"type": "array"},
                                    "candidate_hotels": {"type": "array"},
                                    "layover_minutes": {"type": "integer"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
