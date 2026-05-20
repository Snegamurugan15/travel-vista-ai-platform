import asyncio
import base64
import csv
import os
from pathlib import Path

from Crypto.Cipher import AES
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import DECIMAL, JSON, TIMESTAMP, Column, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATA_DIR = Path(os.getenv("TRAVEL_VISTA_DATA_DIR", "data"))
DATABASE_URL = os.environ["DATABASE_URL"]
AES_KEY = os.getenv("TRAVEL_VISTA_AES_KEY", "dev-only-16-byte").encode("utf-8")[:16].ljust(16, b"0")

metadata = MetaData()

destinations_table = Table(
    "destinations",
    metadata,
    Column("destination_id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("world_wonder", String(255)),
    Column("package_option", String(50)),
    Column("base_price", DECIMAL),
    Column("discount_percentage", Integer),
    Column("transport_modes", JSON),
    Column("dynamic_tags", JSON),
    Column("created_at", TIMESTAMP),
)


def _pad(value: str) -> str:
    pad_length = AES.block_size - len(value.encode("utf-8")) % AES.block_size
    return value + chr(pad_length) * pad_length


def encrypt(value: str) -> str:
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(_pad(value).encode("utf-8"))).decode("utf-8")


async def insert_destinations(session: AsyncSession) -> None:
    with (DATA_DIR / "destinations.csv").open("r", newline="", encoding="utf-8") as csvfile:
        for row in csv.DictReader(csvfile):
            values = {
                "destination_id": int(row["destination_id"]),
                "name": encrypt(row["name"]),
                "world_wonder": row["world_wonder"],
                "package_option": row["package_option"],
                "base_price": float(row["base_price"]),
                "discount_percentage": int(row["discount_percentage"]),
                "transport_modes": row["transport_modes"],
                "dynamic_tags": row["dynamic_tags"],
                "created_at": row["created_at"],
            }
            statement = insert(destinations_table).values(**values).on_conflict_do_nothing(
                index_elements=["destination_id"]
            )
            await session.execute(statement)


async def main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    async with async_session() as session:
        await insert_destinations(session)
        await session.commit()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
