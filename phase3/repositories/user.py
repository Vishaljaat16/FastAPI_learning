
from schemas.user import UserRequest
from models.user import UserTable
from db.database import get_db, AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

router = APIRouter()


@router.post("/add")
async def add_user(
    request: UserRequest,
    db: AsyncSession = Depends(get_db)
):
    # Check whether the requested ID already exists
    result = await db.execute(
        select(UserTable).where(UserTable.id == request.id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this ID already exists"
        )

    # Create and save the user
    new_user = UserTable(**request.model_dump())
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user
