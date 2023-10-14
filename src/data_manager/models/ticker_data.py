import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from .base_model import BaseModel


class TickerData(BaseModel):
    __tablename__ = "ticker_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exchange_id: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column()
    timestamp = Column("timestamp", BigInteger(), nullable=True)
    collected_at: Mapped[Optional[datetime.datetime]] = mapped_column()
    high: Mapped[Optional[float]] = mapped_column()
    low: Mapped[Optional[float]] = mapped_column()
    bid: Mapped[Optional[float]] = mapped_column()
    bidVolume: Mapped[Optional[float]] = mapped_column()
    ask: Mapped[Optional[float]] = mapped_column()
    askVolume: Mapped[Optional[float]] = mapped_column()
    vwap: Mapped[Optional[float]] = mapped_column()
    open: Mapped[Optional[float]] = mapped_column()
    close: Mapped[Optional[float]] = mapped_column()
    last: Mapped[Optional[float]] = mapped_column()
    previousClose: Mapped[Optional[float]] = mapped_column()
    change: Mapped[Optional[float]] = mapped_column()
    percentage: Mapped[Optional[float]] = mapped_column()
    average: Mapped[Optional[float]] = mapped_column()
    baseVolume: Mapped[Optional[float]] = mapped_column()
    quoteVolume: Mapped[Optional[float]] = mapped_column()
    created_at = Column("created_at", DateTime(), server_default=func.now())
