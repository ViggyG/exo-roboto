from datetime import datetime
import asyncio
import json
from asyncio import ensure_future
import ccxt.async_support as ccxt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .models import BaseModel


class DataManager:
    def __init__(
        self,
        exchange_id: str = None,
        params: dict = {},
        sandbox_mode: bool = False,
        database_port: str = None,
        database_host: str = None,
        database_password: str = None,
        database_user: str = None,
        database_db: str = None,
        database_connection_string: str = None,
    ) -> None:
        self.exchange_id = exchange_id
        self.sandbox_mode = sandbox_mode
        self.database_port = database_port
        self.database_host = database_host
        self.database_user = database_user
        self.database_password = database_password
        self.database_db = database_db
        self.database_connection_string = database_connection_string
        self.database_engine = None
        self.database_session: Session = None
        self.exchange = None

        for k, value in params.items():
            if hasattr(self, k):
                setattr(self, k, value)
            else:
                print(f"WARNING class given unknown param {k}")

    @staticmethod
    def create_database_connection_string(user, pwd, host, port, db):
        return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

    async def initialize(self, database_echo: bool = False):
        exchange_class = getattr(ccxt, self.exchange_id, None)

        if not exchange_class:
            raise ValueError(
                "supplied exchange was not found, possibly misspelled or not supported"
            )

        if not self.database_connection_string:
            self.database_connection_string = self.create_database_connection_string(
                self.database_user,
                self.database_password,
                self.database_host,
                self.database_port,
                self.database_db,
            )

        self.exchange: ccxt.Exchange = exchange_class()
        self.exchange.set_sandbox_mode(self.sandbox_mode)
        await self.exchange.load_markets()

        self.database_engine = create_engine(
            self.database_connection_string, echo=database_echo
        )

        self.database_session = Session(self.database_engine)

    async def cleanup(self):
        self.database_session.close()
        await self.exchange.close()

    async def store_ticker_data(self, model: BaseModel):
        """
        Function for collecting ticker data from an exchange
        :param model: the BaseModel representing the data to be inserted into the connected database
        """

        print("Total Symbols: ", len(self.exchange.symbols))

        response_data = await self.exchange.fetch_tickers()

        if not isinstance(response_data, dict):
            raise ValueError(f"Exchange returned non-dict data. Got: {response_data}")

        data_list = []

        for k, value in response_data.items():
            if k in self.exchange.symbols:
                data_list.append(value)

        print("Total Response Symbols: ", len(data_list))

        model.metadata.create_all(bind=self.database_engine)

        for value in data_list:
            if not isinstance(value, dict):
                continue
            data = value
            data["exchange_id"] = self.exchange_id
            data.pop("info")
            date_string = data.pop("datetime", None)
            if date_string:
                data["collected_at"] = datetime.strptime(
                    date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            self.database_session.add(model(**data))

        self.database_session.commit()
