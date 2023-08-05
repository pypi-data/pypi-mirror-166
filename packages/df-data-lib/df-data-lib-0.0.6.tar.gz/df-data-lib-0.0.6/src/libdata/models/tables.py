import sqlalchemy as sa
from sqlalchemy import (
    ForeignKey,
    types,
    BIGINT,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from libdata.models.enums import AccountType, AppType, AuthType, Role
from libdata.settings import settings

Base = declarative_base()


def create_all():
    Base.metadata.create_all(bind=settings.get_engine())


def drop_all():
    Base.metadata.drop_all(bind=settings.get_engine())


def recreate_all():
    Base.metadata.drop_all(bind=settings.get_engine())
    Base.metadata.create_all(bind=settings.get_engine())


class BaseModel(Base):
    __abstract__ = True
    __bind_key__ = "df"

    created = sa.Column(types.TIMESTAMP, server_default=func.now())
    updated = sa.Column(
        types.TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
    created_by = sa.Column(sa.String(), nullable=True)
    updated_by = sa.Column(sa.String(), nullable=True)


class AuditTrailModel(Base):
    __abstract__ = True

    created_by = sa.Column(sa.String(), nullable=True)
    updated_by = sa.Column(sa.String(), nullable=True)


class Model(BaseModel):
    __abstract__ = True

    active = sa.Column(sa.Boolean, nullable=False, server_default="1")
    deleted = sa.Column(sa.Boolean, nullable=False, server_default="0")


class ReqtUser(Model):
    __tablename__ = "reqt_users"

    id = sa.Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    email = sa.Column(sa.String(), nullable=False, unique=True, index=True)
    password = sa.Column(sa.String(), nullable=False)
    app_type = sa.Column(
        sa.Enum(AppType), nullable=True, server_default=AppType.default
    )
    account_type = sa.Column(
        sa.Enum(AccountType), nullable=True, server_default=AccountType.free
    )
    role = sa.Column(
        sa.Enum(Role), nullable=True, server_default=Role.customer
    )
    auth_type = sa.Column(
        sa.Enum(AuthType), nullable=True, server_default=AuthType.default
    )

    user = relationship("User", backref="reqt_users", uselist=False)


class User(Model):
    __tablename__ = "users"

    id = sa.Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    code = sa.Column(sa.String(), nullable=False, unique=True, index=True)
    email = sa.Column(sa.String(), nullable=False, unique=True, index=True)
    signup_completed = sa.Column(sa.Boolean, server_default="0")
    stripe_customer_id = sa.Column(sa.String(), nullable=True, unique=True)
    # TODO: object
    # TODO: metadata

    reqt_user_id = sa.Column(
        BIGINT, ForeignKey("reqt_users.id"), nullable=False, unique=True
    )
    profile = relationship("Profile", backref="users", uselist=False)


class Profile(Model):
    __tablename__ = "profiles"

    id = sa.Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    full_name = sa.Column(sa.String())
    company_name = sa.Column(sa.String(), nullable=True)
    city = sa.Column(sa.String(), nullable=True)
    state = sa.Column(sa.String(), nullable=True)
    phone = sa.Column(sa.String(), nullable=True)
    address_line1 = sa.Column(sa.String(), nullable=True)

    user_id = sa.Column(
        BIGINT, ForeignKey("users.id"), nullable=True, unique=True
    )
