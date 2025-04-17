from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Reservation


async def is_reservation_conflict(
        db: AsyncSession, table_id: int, reservation_time: datetime, duration_minutes: int) -> bool:
    end_time = reservation_time + timedelta(minutes=duration_minutes)

    query = select(Reservation).where(
        and_(
            Reservation.table_id == table_id,
            Reservation.reservation_time < end_time,
            (Reservation.reservation_time + Reservation.duration_minutes * timedelta(minutes=1)) > reservation_time
        )
    )

    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def get_reservations_service(db: AsyncSession):
    result = await db.execute(select(Reservation))
    return result.scalars().all()


async def create_reservation_service(reservation, db):
    has_conflict = await is_reservation_conflict(
        db=db,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes
    )

    if has_conflict:
        raise HTTPException(status_code=400, detail='Table is already reserved for this time slot')

    new_reservation = Reservation(**reservation.model_dump())
    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)
    return new_reservation


async def delete_reservation_service(reservation_id, db):
    result = await db.execute(select(Reservation).where(Reservation.id == reservation_id))
    reservation = result.scalar_one_or_none()
    if not reservation:
        raise HTTPException(status_code=404, detail='Reservation not found')
    await db.delete(reservation)
    await db.commit()
    return {'detail': 'Reservation deleted'}
