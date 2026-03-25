from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class ContactCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None


contacts = [
    {
        "id": 1,
        "name": "山田太郎",
        "email": "taro@example.com",
        "subject": "お問い合わせテスト",
        "message": "これはテストです",
        "status": "未対応"
    }
]


@app.get("/contacts")
def get_contacts():
    return contacts


@app.get("/contacts/{id}")
def get_contact(id: int):
    for contact in contacts:
        if contact["id"] == id:
            return contact
    return {"message": "指定されたお問い合わせは見つかりません"}


@app.post("/contacts")
def create_contact(contact: ContactCreate):
    new_id = len(contacts) + 1
    new_contact = {
        "id": new_id,
        "name": contact.name,
        "email": contact.email,
        "subject": contact.subject,
        "message": contact.message,
        "status": "未対応"
    }
    contacts.append(new_contact)
    return new_contact


@app.patch("/contacts/{id}")
def update_contact(id: int, contact_update: ContactUpdate):
    for contact in contacts:
        if contact["id"] == id:
            update_data = contact_update.model_dump(exclude_unset=True)
            contact.update(update_data)
            return contact
    return {"message": "指定されたお問い合わせは見つかりません"}
