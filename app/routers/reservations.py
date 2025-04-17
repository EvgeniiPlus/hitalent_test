from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.schemas import ReservationCreate, ReservationOut
from app.services.reservation_service import get_reservations_service, \
    create_reservation_service, delete_reservation_service

router = APIRouter()


@router.get('/', response_model=list[ReservationOut])
async def get_reservations(db: AsyncSession = Depends(get_session)):
    return await get_reservations_service(db)


@router.post('/', response_model=ReservationOut, status_code=201)
async def create_reservation(reservation: ReservationCreate, db: AsyncSession = Depends(get_session)):
    return await create_reservation_service(reservation, db)


@router.delete('/{reservation_id}', status_code=204)
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_session)):
    return await delete_reservation_service(reservation_id, db)
