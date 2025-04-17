from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.models import Table


async def get_tables_service(db):
    result = await db.execute(select(Table))
    return result.scalars().all()


async def create_tables_service(table, db):
    new_table = Table(**table.model_dump())
    db.add(new_table)
    try:
        await db.commit()
        await db.refresh(new_table)
        return new_table
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail='Table already exists')


async def delete_tables_service(table_id, db):
    result = await db.execute(select(Table).where(Table.id == table_id))
    table = result.scalar_one_or_none()
    if not table:
        raise HTTPException(status_code=404, detail='Table not found')
    await db.delete(table)
    await db.commit()
    return {'detail': 'Table deleted'}
