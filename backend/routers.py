from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import Resume, User
from .schemas import ResumeCreate, ResumeUpdate, ResumeInDB, ResumeInput
from .schemas import UserCreate, UserInDB, UserUpdate, Token
from .database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from .jwt_Authentication import (
    login_for_access_token,
    create_access_token,
    get_password_hash,
    ACCESS_TOKEN_EXPIRES_MINUTES,
)
from datetime import datetime, timedelta
from .jwt_Authentication import get_current_user


router = APIRouter(prefix="/resumes", tags=["resumes"])
user_router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/get_list",
    response_model=list[ResumeInDB],
    summary="Получение списка всех резюме авторизованного пользователя",
)
def get_list_of_resumes(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_id = current_user.id
    query = db.execute(select(Resume).where(Resume.user_id == user_id)).scalars().all()
    return query


@router.get(
    "/{resume_id}",
    response_model=ResumeInDB,
    summary="Получение конкретного резюме по ID",
)
def get_one_resume(
    resume_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_id = current_user.id
    query = select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    resume = db.execute(query).scalar()
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Резюме не найдено"
        )
    return resume


@router.post("/", response_model=ResumeInDB, summary="Создание нового резюме")
def create_resume(
    new_resume: ResumeCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_id = current_user.id
    resume_data = new_resume.model_dump()
    resume_data["user_id"] = user_id
    resume = Resume(**resume_data)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.patch(
    "/{resume_id}",
    response_model=ResumeInDB,
    summary="Обновление и улучшение конкретного резюме по ID",
)
def update_old_resume(
    resume_id: int,
    resume_to_update: ResumeUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):

    user_id = current_user.id
    update_data = resume_to_update.model_dump(exclude_unset=True)
    query = (
        update(Resume)
        .where(Resume.id == resume_id, Resume.user_id == user_id)
        .values(update_data)
    )
    result = db.execute(query)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Резюме не найдено"
        )
    db.commit()
    new_query = select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    updated_resume = db.execute(new_query).scalar()
    return updated_resume


@router.delete("/delete_all", summary="Удаление всех резюме")
def delete_all_resumes(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_id = current_user.id

    query = delete(Resume).where(Resume.user_id == user_id)
    result = db.execute(query)
    db.commit()
    return {"message": "Все резюме успешно удалены"}


@router.delete("/{resume_id}", summary="Удаление конкретного реюме по ID")
def delete_one_resume(
    resume_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_id = current_user.id
    query = delete(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    result = db.execute(query)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данное резюме с таким ID не найдено",
        )
    return {"message": "Резюме успешно удалено"}


@router.post(
    "/{resume_id}/improve",
    response_model=ResumeInDB,
    summary="Улучшение резюме через AI",
)
def improve_resume_by_ai(
    resume_id: int,
    resume_input: ResumeInput,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    user_id = current_user.id
    query = select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    resume_to_update = db.execute(query).scalar()
    improved_content = resume_input.content
    improved_content += " [Improved] "
    resume_to_update.content = improved_content
    db.add(resume_to_update)
    db.commit()
    db.refresh(resume_to_update)
    return resume_to_update


@user_router.post(
    "/registration",
    response_model=Token,
    summary="Для регистрации нового пользователя и получения токена",
)
def registration(new_user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.email == new_user.email)
    existing_user = db.execute(query).scalar()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    hashed_password = get_password_hash(new_user.password)
    user = User(email=new_user.email, hash_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post(
    "/token", response_model=Token, summary="Для авторизации существующего пользователя"
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return login_for_access_token(form_data=form_data, db=db)
