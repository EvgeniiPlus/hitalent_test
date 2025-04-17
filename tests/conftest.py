import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.db.session import get_session
from app.main import app
from app.models.models import Base


@pytest.fixture(scope='session')
def anyio_backnd():
    return 'asyncio'


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def db_engine():
    return create_async_engine(settings.TEST_DATABASE_URL, echo=False)


@pytest.fixture(scope='session')
def async_session_maker(db_engine):
    return async_sessionmaker(bind=db_engine, expire_on_commit=False)

@pytest.fixture(autouse=True, scope="function")
async def clear_db(db_engine):
    async with db_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
    yield


@pytest.fixture(scope='function')
async def async_client(async_session_maker):
    async def override_get_db():
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
