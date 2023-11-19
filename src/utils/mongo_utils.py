# mypy: disable-error-code="attr-defined"

import os
from datetime import datetime, timedelta
from typing import List, Optional

import mongoengine

from src.db_models.tumatura import Roles, UserRole, Users


class MongoUtils:
    def __init__(self) -> None:
        mongoengine.connect(host=os.getenv("MONGO_CONNECTION_STRING"))

    @staticmethod
    def get_all_user_data() -> List[Users]:
        return Users.objects()

    @staticmethod
    def get_user_data(*, customer_id: Optional[int] = None, discord_name: str, email: Optional[str] = None) -> Users:
        user = None
        if customer_id:
            user = Users.objects(customer_id=customer_id).first()
        if user is None and discord_name:
            user = Users.objects(discord=discord_name).first()
        if user is None and email:
            user = Users.objects(email=email).first()

        return user if user is not None else Users()

    @staticmethod
    def get_role_id_by_name(role_name: str) -> int:
        return Roles.objects(role_name=role_name).first().role_id

    def upsert_user_role(
        self,
        role_id: List[int],
        discord_name: str,
        *,
        customer_id: Optional[int] = None,
        email: Optional[str] = None,
        expiration_date: Optional[datetime] = None,
    ) -> None:
        user_data = self.get_user_data(customer_id=customer_id, discord_name=discord_name, email=email)

        user_data.customer_id = customer_id if customer_id else user_data.customer_id
        user_data.email = email if email else user_data.email
        user_data.discord = discord_name if discord_name else user_data.discord

        if existing_role_record_pos := next(
            (i for i, role_record in enumerate(user_data.roles) if role_record.role_id == role_id), None
        ):
            del user_data.roles[existing_role_record_pos]

        for role in role_id:
            role_record = UserRole(
                role_id=role, exp_date=expiration_date if expiration_date else (datetime.now() + timedelta(weeks=1))
            )
            user_data.roles.append(role_record)

        user_data.save()

    def upsert_user_data(
        self, discord_name: str, customer_id: Optional[int] = None, email: Optional[str] = None
    ) -> None:
        user_data = self.get_user_data(customer_id=customer_id, discord_name=discord_name, email=email)

        user_data.customer_id = customer_id if customer_id else user_data.customer_id
        user_data.email = email if email else user_data.email
        user_data.discord = discord_name if discord_name else user_data.discord

        user_data.save()

    def remove_user_role(self, discord_nick: str, role_id: int) -> None:
        user_data = self.get_user_data(discord_name=discord_nick)

        if existing_role_record_pos := next(
            (i for i, role_record in enumerate(user_data.roles) if role_record.role_id == role_id), None
        ):
            del user_data.roles[existing_role_record_pos]

        user_data.save()

    def clean_expired_user_roles(self) -> None:
        all_users = self.get_all_user_data()

        for user in all_users:
            for role in user.roles:
                if role.exp_date < datetime.now():
                    user.roles.remove(role)
            user.save()


mongo_utils = MongoUtils()
