"""
Agentic Travel Multi-Leg Itinerary Synthesizer (Zero External Dependencies)
Provides multi-leg flight assembly, layover risk calculation, lodging optimization, and booking manifests.
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

class AgenticTravelItinerarySynthesizer:
    def __init__(self, min_domestic_layover: int = 45, min_intl_layover: int = 90):
        self.min_dom_layover = min_domestic_layover
        self.min_intl_layover = min_intl_layover

    def evaluate_layover_risk(
        self,
        layover_minutes: int,
        is_international: bool = False,
        requires_terminal_transfer: bool = False
    ) -> Dict[str, Any]:
        """Calculates missed-connection probability and risk classification."""
        threshold = self.min_intl_layover if is_international else self.min_dom_layover
        if requires_terminal_transfer:
            threshold += 30

        delta = layover_minutes - threshold
        if delta < 0:
            risk_level = "CRITICAL_MISS_CONNECTION_PROBABLE"
            risk_score = 0.95
            safe = False
        elif delta <= 20:
            risk_level = "TIGHT_CONNECTION_RISKY"
            risk_score = 0.65
            safe = True
        elif delta <= 60:
            risk_level = "OPTIMAL_COMFORTABLE"
            risk_score = 0.15
            safe = True
        else:
            risk_level = "EXCESSIVE_LONG_LAYOVER"
            risk_score = 0.30
            safe = True

        return {
            "layover_minutes": layover_minutes,
            "required_safe_threshold_minutes": threshold,
            "safe_to_book": safe,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "advisory": (
                "Layover is below minimum safety threshold. Recommend alternative flight segment."
                if not safe else "Connection time is sufficient for checked bag transfer and customs."
            )
        }

    def calculate_lodging_options(
        self,
        candidate_hotels: List[Dict[str, Any]],
        nights: int = 3,
        travelers: int = 2
    ) -> Dict[str, Any]:
        """Ranks candidate hotels by location proximity, guest ratings, and total net rate."""
        if not candidate_hotels:
            return {"hotels": []}

        scored = []
        for h in candidate_hotels:
            name = h.get("name", "Hotel")
            nightly_rate = float(h.get("nightly_rate", 150.0))
            cleaning_fee = float(h.get("cleaning_fee", 0.0))
            tax_rate = float(h.get("tax_rate", 0.14)) # 14% hotel occupancy tax
            rating = float(h.get("rating", 4.0)) # out of 5.0
            distance_to_center_km = float(h.get("distance_to_center_km", 3.0))

            room_subtotal = nightly_rate * nights
            total_cost = room_subtotal * (1.0 + tax_rate) + cleaning_fee

            # Proximity score (1.0 for <=1km, decays down to 0.2 for 15km+)
            prox_score = max(0.2, 1.0 - (distance_to_center_km / 20.0))
            # Rating score
            rating_score = rating / 5.0
            # Value ratio
            cost_per_person_per_night = total_cost / (nights * travelers)

            composite_score = 0.40 * rating_score + 0.35 * prox_score + 0.25 * max(0.1, 1.0 - (cost_per_person_per_night / 300.0))

            scored.append({
                "name": name,
                "nightly_rate": round(nightly_rate, 2),
                "total_cost_usd": round(total_cost, 2),
                "cost_per_person_night": round(cost_per_person_per_night, 2),
                "rating": rating,
                "distance_km": distance_to_center_km,
                "composite_score": round(composite_score, 4)
            })

        scored.sort(key=lambda x: x["composite_score"], reverse=True)
        return {
            "total_analyzed": len(candidate_hotels),
            "nights": nights,
            "top_lodging_choice": scored[0] if scored else None,
            "ranked_hotels": scored
        }

    def synthesize_itinerary(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str,
        budget_usd: float,
        travelers_count: int = 1,
        candidate_flights: Optional[List[Dict[str, Any]]] = None,
        candidate_hotels: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes a complete multi-leg end-to-end trip itinerary combining flights,
        lodging, layover buffers, and budget constraints.
        """
        candidate_flights = candidate_flights or []
        candidate_hotels = candidate_hotels or []

        # 1. Pick optimal flight
        best_flight = None
        if candidate_flights:
            valid_flights = []
            for f in candidate_flights:
                price = float(f.get("total_price", 500.0)) * travelers_count
                layovers = f.get("layovers", [])
                safe_flight = True
                for l in layovers:
                    mins = l.get("duration_minutes", 60)
                    is_intl = l.get("is_international", False)
                    risk = self.evaluate_layover_risk(mins, is_intl)
                    if not risk["safe_to_book"]:
                        safe_flight = False
                        break
                if safe_flight:
                    valid_flights.append((f, price))
            if valid_flights:
                valid_flights.sort(key=lambda x: x[1])
                best_flight = valid_flights[0][0]
                flight_cost = valid_flights[0][1]
            else:
                best_flight = candidate_flights[0]
                flight_cost = float(best_flight.get("total_price", 500.0)) * travelers_count
        else:
            best_flight = {
                "airline": "Direct Partner Airlines",
                "outbound": f"{origin} -> {destination} on {departure_date}",
                "inbound": f"{destination} -> {origin} on {return_date}",
                "total_price": round(budget_usd * 0.45 / travelers_count, 2)
            }
            flight_cost = float(best_flight["total_price"]) * travelers_count

        # 2. Pick lodging
        remaining_budget = max(0.0, budget_usd - flight_cost)
        nights = 3 # default estimate
        lodging_analysis = self.calculate_lodging_options(candidate_hotels, nights=nights, travelers=travelers_count)
        best_hotel = lodging_analysis.get("top_lodging_choice") or {
            "name": f"Centric Boutique Hotel {destination}",
            "total_cost_usd": round(min(remaining_budget * 0.70, 600.0), 2),
            "nightly_rate": round(min(remaining_budget * 0.70, 600.0) / nights, 2),
            "rating": 4.7
        }
        hotel_cost = best_hotel["total_cost_usd"]

        # 3. Compile totals & feasibility
        grand_total = flight_cost + hotel_cost
        within_budget = grand_total <= budget_usd
        itinerary_token = "GP-TRIP-" + hashlib.sha256(f"{origin}{destination}{departure_date}{grand_total}".encode("utf-8")).hexdigest()[:16]

        return {
            "itinerary_id": itinerary_token,
            "route": f"{origin} ⇄ {destination}",
            "dates": {"departure": departure_date, "return": return_date},
            "travelers": travelers_count,
            "budget": {
                "target_budget_usd": budget_usd,
                "flight_cost_usd": round(flight_cost, 2),
                "lodging_cost_usd": round(hotel_cost, 2),
                "grand_total_usd": round(grand_total, 2),
                "surplus_or_deficit": round(budget_usd - grand_total, 2),
                "within_budget": within_budget
            },
            "selected_flight": best_flight,
            "selected_lodging": best_hotel,
            "status": "READY_FOR_COMMERCE_HOLD"
        }

    def compile_booking_manifest(self, itinerary: Dict[str, Any]) -> Dict[str, Any]:
        """Assembles a formal multi-party booking payload for checkout."""
        return {
            "manifest_type": "TRAVEL_CONSOLIDATED_CHECKOUT",
            "itinerary_id": itinerary.get("itinerary_id"),
            "route": itinerary.get("route"),
            "authorized_payment_total": itinerary.get("budget", {}).get("grand_total_usd"),
            "reservation_items": [
                {"type": "FLIGHT", "item": itinerary.get("selected_flight")},
                {"type": "LODGING", "item": itinerary.get("selected_lodging")}
            ],
            "cancellation_terms": "24-hour full refund hold via Agentic Commerce Mandate"
        }
