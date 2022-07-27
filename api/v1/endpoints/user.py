from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError


from core.deps import get_session, get_current_user
from core.security import generate_hash_password
from core.auth import auth, create_token_access

from sqlmodel import select

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()

# GET logged
@router.get('/logged', response_model=UserSchemaBase)
def get_logged(user_logged: UserModel = Depends(get_current_user)):
    return user_logged


# POST User
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchemaCreate)
async def post_user(user: UserModel, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(
        name=user.name, 
        email=user.email, 
        password=generate_hash_password(user.password), 
        is_admin=user.is_admin
    )

    try:
        db.add(new_user)
        await db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='There is already a user with this registered email.'
        )

    return new_user


# GET users
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(user_logged: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().all()

        return users


# GET user
@router.get('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, user_logged: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserModel = result.scalar_one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail='User not found',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT user
@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserSchemaUpdate)
async def put_user(user_id: int, user: UserModel, user_logged: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_update: UserModel = result.scalar_one_or_none()

        if user_update:
            user_update.name = user.name
            user_update.email = user.email
            user_update.password = user.password
            user_update.is_admin = user.is_admin

            await session.commit()

            return user_update
        else:
            raise HTTPException(detail='User not found',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE user
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_logged: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_delete: UserModel = result.scalar_one_or_none()

        if not user_logged.is_admin:
            raise HTTPException(detail='User not permission',
                                status_code=status.HTTP_403_FORBIDDEN)

        if user_delete:
            await session.delete(user_delete)
            await session.commit()

            # Colocamos por conta de um bug no FastAPI
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='User not found',
                                status_code=status.HTTP_404_NOT_FOUND)

# POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await auth(email=form_data.username, password=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='data no correct.')

    return JSONResponse(content={"access_token": create_token_access(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
