

from fastapi import APIRouter
from backend.db import db

router = APIRouter()

@router.post("/dialogflow")
async def dialogflow(payload: dict):
    intent = payload.get("queryResult", {}).get("intent", {}).get("displayName")
    params = payload.get("queryResult", {}).get("parameters", {})

    if intent == "create_ticket":
        ticket = {
            "subject": params.get("subject", "General issue"),
            "description": params.get("description", "N/A"),
            "category": params.get("category", "general"),
            "priority": params.get("priority", "medium"),
            "status": "open",
            "created_by": "chatbot_user"
        }
        res = await db.tickets.insert_one(ticket)
        return {"fulfillmentText": f"✅ Ticket created! ID: {res.inserted_id}"}

    if intent == "check_status":
        id_ = params.get("ticket_id")
        if not id_:
            return {"fulfillmentText": "Please provide a ticket ID."}
        from bson import ObjectId
        try:
            _id = ObjectId(id_)
        except Exception:
            return {"fulfillmentText": "Invalid ticket ID format."}
        ticket = await db.tickets.find_one({"_id": _id})
        if not ticket:
            return {"fulfillmentText": "Ticket not found."}
        return {"fulfillmentText": f"Ticket {id_} is {ticket.get('status','open')}"}

    return {"fulfillmentText": "Sorry, I could not process your request."}
