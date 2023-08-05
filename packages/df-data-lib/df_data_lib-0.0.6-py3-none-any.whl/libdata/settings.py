from sqlalchemy.orm import scoped_session, sessionmaker

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.engine import create_engine
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")
    # database_async_url: str = Field(env='DATABASE_ASYNC_URL')

    def get_session(self):
        db_session = scoped_session(
            sessionmaker(
                autocommit=True, autoflush=False, bind=self.get_engine()
            )
        )

        assert db_session
        return db_session

    def get_engine(self):
        try:
            assert self.database_url
            engine = create_engine(self.database_url)
            return engine
        except AssertionError as assertion_error:
            print(assertion_error)
        return None

    # def get_async_session(self):
    #     db_async_session = scoped_session(sessionmaker(
    #         autocommit=True,
    #         autoflush=False,
    #         bind=self.get_async_engine()
    #     ))

    #     assert db_async_session
    #     return db_async_session

    # def get_async_engine(self):
    #     try:
    #         assert self.database_async_url
    #         async_engine = create_async_engine(self.database_async_url)
    #         return async_engine
    #     except AssertionError as assertion_error:
    #         print(assertion_error)
    #     return None


settings = Settings()
