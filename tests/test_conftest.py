# test_users.py

from builtins import len
import pytest
from httpx import AsyncClient
from sqlalchemy.future import select

from app.models.user_model import User, UserRole
from app.utils.security import verify_password

@pytest.mark.asyncio
async def test_user_creation(db_session, user):
    """Test that a user is correctly created and stored in the database."""
    result = await db_session.execute(select(User).filter_by(email=user.email))
    stored_user = result.scalars().first()
    assert stored_user is not None
    assert stored_user.username == user.username
    assert verify_password("MySuperPassword$1234", stored_user.hashed_password)

# Apply similar corrections to other test functions
@pytest.mark.asyncio
async def test_locked_user(db_session, locked_user):
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    stored_user = result.scalars().first()
    assert stored_user.is_locked

@pytest.mark.asyncio
async def test_verified_user(db_session, verified_user):
    result = await db_session.execute(select(User).filter_by(email=verified_user.email))
    stored_user = result.scalars().first()
    assert stored_user.email_verified

@pytest.mark.asyncio
async def test_password_hashing(user):
    assert verify_password("MySuperPassword$1234", user.hashed_password)

@pytest.mark.asyncio
async def test_user_unlock(db_session, locked_user):
    locked_user.unlock_account()
    await db_session.commit()
    result = await db_session.execute(select(User).filter_by(email=locked_user.email))
    updated_user = result.scalars().first()
    assert not updated_user.is_locked
