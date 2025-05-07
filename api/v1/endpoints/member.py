from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.configs import settings
from models.member_model import MemberModel
from schemas.member_schema import MemberSchemaBase, MemberSchemaCreated, MemberSchemaUpdated
from core.deps import get_session
from core.security import generate_password_hash
from core.auth import authenticate_member, create_access_token

import re

router = APIRouter()

password_regex: str = "^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{7,})\S$"
email_regex: str = "^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"

logged_in_user_token: str = ''
member_cookie = None

#POST member (criar conta)
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=MemberSchemaBase)
async def post_new_member(member: MemberSchemaCreated, db: AsyncSession = Depends(get_session)):

    if not re.search(password_regex, member.password_u):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password too weak (needs lower case, upper case, a number and at least 8 characters)")
    if not re.search(email_regex, member.email_u):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid email address")

    import uuid

    new_token: str = None
    async with db as session:
        query = select(MemberModel).filter(MemberModel.email_u == member.email_u)
        result = await session.execute(query)
        unique_email_check = result.scalar_one_or_none()

        if unique_email_check:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email is already in use")


        while True:
            new_token: str = uuid.uuid4()
            query = select(MemberModel).filter(MemberModel.token_u == str(new_token))
            result = await session.execute(query)
            unique_token_check = result.scalar_one_or_none()
            if not unique_token_check:
                break

    new_member: MemberModel = MemberModel(
        name_u=member.name_u,
        email_u=member.email_u,
        password_u=generate_password_hash(member.password_u),
        is_premium_u=False,
        token_u=str(new_token)
    )

    async with db as session:
        session.add(new_member)
        await session.commit()
        return new_member

#POST member (logar)
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    member = await authenticate_member(email=form_data.username, password=form_data.password, db=db)
    if not member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    logged_in_user_token = create_access_token(subject=member.token_u)
    response = JSONResponse(content={"access_token": logged_in_user_token, "token_type": "bearer"}, status_code=status.HTTP_200_OK)
    response.set_cookie(key="access_token", value=f"{logged_in_user_token}", path=f"{settings.API_V1_SRT}/members/account", httponly=True)
    return response

#GET member (ver membro logado)
@router.get('/account', response_model=MemberSchemaBase)
async def get_account(request: Request, db: AsyncSession = Depends(get_session)):
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    from jose import jwt, JWTError

    try:
        payload = jwt.decode(
            request.cookies.get("access_token"),
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    async with db as session:
        query = select(MemberModel).filter(MemberModel.token_u == username)
        result = await session.execute(query)
        member = result.scalar_one_or_none()

        if member:
            return member

        raise credentials_exception

'''
#GET members
@router.get('/', response_model=List[MemberSchemaBase])
async def get_members(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MemberModel)
        result = await session.execute(query)
        members: List[MemberModel] = result.scalars().all()

        return members

#GET member
@router.get('/{member_id}', response_model=MemberSchemaBase, status_code=status.HTTP_200_OK)
async def get_member(member_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MemberModel).filter(MemberModel.id_u == member_id)
        result = await session.execute(query)
        member = result.scalar_one_or_none()

        if member:
            return member
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

#PUT member
@router.put('/{member_id}', response_model=MemberSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_member(member_id: int, member: MemberSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MemberModel).filter(MemberModel.id == member_id)
        result = await session.execute(query)
        member_up = result.scalars().unique().one_or_none()

        if member_up:
            if member.name_u:
                member_up.name_u = member.name_u
            if member.email_u:
                member_u.email_u = member.email_u
            if member.password_u:
                member_up.password_u = generate_password_hash(member.password_u)

            await session.commit()

            return member_up
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

#DELETE member
@router.delete('/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(member_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MemberModel).filter(MemberModel.id == member_id)
        result = await session.execute(query)
        member_del = result.scalar_one_or_none()

        if member_del:
            await session.delete(member_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")'''