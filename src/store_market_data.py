from time import perf_counter
import asyncio
from data_manager import DataManager
from data_manager.models import TickerData
from config import app_config


async def main():
    total_start_time = perf_counter()

    dtm = DataManager(params=app_config.data_manager_params)
    await dtm.initialize(database_echo=False)
    await dtm.store_ticker_data(TickerData)
    await dtm.cleanup()

    print(f"Total execution time {perf_counter() - total_start_time}")


if __name__ == "__main__":
    asyncio.run(main())
