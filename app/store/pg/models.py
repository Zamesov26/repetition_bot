from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from sqlalchemy import MetaData

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Model(MappedAsDataclass, DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)

def generate_enum(python_enum: type[Enum]) -> sa.Enum:
    return sa.Enum(
        python_enum,
        native_enum=False,
        validate_strings=True,
        values_callable=lambda enum: [field.value for field in enum],
    )
