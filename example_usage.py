"""Example usage for AgenticTravelItinerarySynthesizer."""
import json
from client import AgenticTravelItinerarySynthesizer

def main():
    print("=== Agentic Travel Multi-Leg Itinerary Synthesizer Demo ===")
    engine = AgenticTravelItinerarySynthesizer()

    # 1. Synthesize multi-leg flight + hotel package within budget
    hotels = [
        {"name": "Shinjuku Granbell", "nightly_rate": 160.0, "rating": 4.5, "distance_to_center_km": 1.2},
        {"name": "Ginza Grand Luxury", "nightly_rate": 320.0, "rating": 4.9, "distance_to_center_km": 0.5},
        {"name": "Ueno Capsule Pod", "nightly_rate": 45.0, "rating": 3.9, "distance_to_center_km": 4.8}
    ]

    print("\n--- 1. Synthesizing Tokyo Trip Itinerary (Meta Muse / Expedia Integration) ---")
    trip = engine.synthesize_itinerary(
        origin="SFO",
        destination="HND",
        departure_date="2026-10-15",
        return_date="2026-10-19",
        budget_usd=2200.0,
        travelers_count=2,
        candidate_hotels=hotels
    )
    print(json.dumps(trip, indent=2))

    # 2. Layover Risk Analysis
    print("\n--- 2. Evaluating International Layover Connection Risk ---")
    tight_layover = engine.evaluate_layover_risk(layover_minutes=55, is_international=True)
    print(f"Layover: 55 min -> Safe: {tight_layover['safe_to_book']}, Level: {tight_layover['risk_level']}")

    safe_layover = engine.evaluate_layover_risk(layover_minutes=110, is_international=True)
    print(f"Layover: 110 min -> Safe: {safe_layover['safe_to_book']}, Level: {safe_layover['risk_level']}")

if __name__ == "__main__":
    main()
