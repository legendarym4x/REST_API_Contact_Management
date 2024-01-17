from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta

from src.entity.models import Contact
from src.schemas.schemas import ContactModel


async def get_contacts(skip: int, limit: int, db: AsyncSession):
    query = select(Contact).offset(skip).limit(limit)
    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts


async def get_contact_by_id(contact_id: int, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id)
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    return contact


async def search_contacts(
    db: AsyncSession, limit: int, offset: int, name: str = None, surname: str = None, email: str = None
):
    query = select(Contact).offset(offset).limit(limit)
    if name:
        query = query.filter(Contact.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(Contact.surname.ilike(f"%{surname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts


async def get_contacts_with_birthdays(days: int, db: AsyncSession):
    today = datetime.today().date()
    start = today.strftime('%m-%d')
    end = (today + timedelta(days)).strftime('%m-%d')
    query = select(Contact).filter(func.to_char(Contact.birthday, 'MM-DD').between(start, end))
    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts


async def create_contact(body: ContactModel, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id)
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    query = select(Contact).filter_by(id=contact_id)
    result = await db.execute(query)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
