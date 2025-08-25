
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.db import db
from backend.auth import get_current_user
from backend.models.ticket import TicketIn, TicketOut
from backend.models.message import MessageIn
from bson import ObjectId

router = APIRouter()

def oid(id: str):
    try:
        return ObjectId(id)
    except Exception:
        return None

def serialize(doc: dict) -> dict:
    if not doc:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.post("/", response_model=dict)
async def create_ticket(ticket: TicketIn, user=Depends(get_current_user)):
    doc = ticket.model_dump()
    # naive auto category
    desc = doc.get("description","").lower()
    if any(k in desc for k in ["wifi","internet","login","computer"]):
        doc["category"] = "it"
    elif any(k in desc for k in ["fees","refund","payment"]):
        doc["category"] = "finance"
    elif any(k in desc for k in ["hostel","warden","room"]):
        doc["category"] = "hostel"
    doc["created_by"] = user["id"]
    res = await db.tickets.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.get("/", response_model=List[dict])
async def list_tickets(user=Depends(get_current_user)):
    filt = {} if user.get("role") in ["agent","admin"] else {"created_by": user["id"]}
    cursor = db.tickets.find(filt).sort([("_id", -1)])
    items = []
    async for t in cursor:
        items.append(serialize(t))
    return items

@router.get("/{id}", response_model=dict)
async def get_ticket(id: str, user=Depends(get_current_user)):
    _id = oid(id)
    if not _id:
        raise HTTPException(status_code=400, detail="Invalid id")
    t = await db.tickets.find_one({"_id": _id})
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    if user.get("role") == "user" and t.get("created_by") != user["id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return serialize(t)

@router.patch("/{id}", response_model=dict)
async def update_ticket(id: str, patch: dict, user=Depends(get_current_user)):
    if user.get("role") not in ["agent","admin"]:
        raise HTTPException(status_code=403, detail="Agents only")
    _id = oid(id)
    await db.tickets.update_one({"_id": _id}, {"$set": patch})
    t = await db.tickets.find_one({"_id": _id})
    return serialize(t)

@router.post("/{id}/messages", response_model=dict)
async def add_message(id: str, msg: MessageIn, user=Depends(get_current_user)):
    _id = oid(id)
    t = await db.tickets.find_one({"_id": _id})
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if user.get("role") == "user" and t.get("created_by") != user["id"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    doc = {"ticket_id": str(_id), "author": user["id"], "from": "agent" if user.get("role") in ["agent","admin"] else "user", "text": msg.text}
    res = await db.messages.insert_one(doc)
    return {"id": str(res.inserted_id), **doc}

