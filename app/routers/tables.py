from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.schemas import TableCreate, TableOut
from app.services.table_service import get_tables_service, create_tables_service, delete_tables_service

router = APIRouter()


@router.get('/', response_model=list[TableOut])
async def get_tables(db: AsyncSession = Depends(get_session)):
    return await get_tables_service(db)


@router.post('/', response_model=TableOut, status_code=201)
async def create_table(table: TableCreate, db: AsyncSession = Depends(get_session)):
    return await create_tables_service(table, db)


@router.delete('/{table_id}', status_code=204)
async def delete_table(table_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_tables_service(table_id, db)
