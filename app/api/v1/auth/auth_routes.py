from typing import cast

from fastapi import APIRouter, Body
from pydantic import UUID4
from typing_extensions import TypedDict

from app.api.v1.auth.auth_exeptions import AuthApiError, SupabaseException
from app.api.v1.auth.auth_schema import LoginSchema, RegisterSchema
from app.middlewares.auth_handler import signJWT
from app.repositories.supabase import supabase

router = APIRouter(prefix="/auth", tags=["auth"])

LoginResponse = TypedDict(
    "LoginResponse", {"user": str | UUID4, "access_token_supabase": str, "access_token_dressup": str})


@router.post("/login")
def login(signin: LoginSchema = Body(...)) -> LoginResponse:
    try:
        res = supabase.auth.sign_in_with_password(
            credentials={"email": signin.email, "password": signin.password})

        access_token_supabase = res.session.access_token if res.session is not None else ""
        user_id = res.user.id if res.user is not None else ""

        access_token, _ = signJWT(user_id, keyType="PUBLIC",
                                  role="ADMIN", exp_time_sec=3600)

        return {"user": user_id, "access_token_supabase": access_token_supabase, "access_token_dressup": access_token}
    except Exception as e:
        raise SupabaseException(cast(AuthApiError, e))


@router.post("/register")
def register(register_data: RegisterSchema = Body(...)):
    print(register_data)

    try:
        res = supabase.auth.sign_up(
            credentials={
                "email": register_data.email,
                "password": register_data.password,
                "options": {
                    "data": {
                        "ruc": register_data.ruc,
                        "names": register_data.names,
                        "lastnames": register_data.lastnames,
                        "email": register_data.email,
                        "phone": register_data.phone,
                        "role": register_data.role,
                        "status": register_data.status,
                    }
                }
            }
        )

        print(res)
        return {"message": "register success"}
    except Exception as e:
        raise SupabaseException(cast(AuthApiError, e))
