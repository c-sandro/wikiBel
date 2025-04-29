from typing import List, Optional, Any

from Tools.i18n.msgfmt import generate
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.member_model import MemberModel
from schemas.member_schema import MemberSchemaBase, MemberSchemaCreated, MemberSchemaUpdated
from core.deps import get_session, get_current_member
from core.security import generate_password_hash
from core.auth import authenticate_member, create_access_token

router = APIRouter()

#POST member (criar conta)
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=MemberSchemaBase)
async def post_new_member(member: MemberSchemaCreated, db: AsyncSession = Depends(get_session)):
    new_member: MemberModel = MemberModel(
        name_u=member.name_u,
        email_u=member.email_u,
        password_u=generate_password_hash(member.password_u),
        is_premium_u=False
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

    return JSONResponse(content={"acess_token": create_access_token(subject=member.id_u), "token_type": "bearer"}, status_code=status.HTTP_200_OK)

#GET member (ver membro logado)
@router.get('/account', response_model=MemberSchemaBase)
def get_logged_in_member(logged_in_member: MemberModel = Depends(get_current_member)):
    return logged_in_member

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
        query = select(MemberModel).filter(MemberModel.id == member_id)
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