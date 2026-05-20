# rds_insert_async.py
import asyncio, csv, base64
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, Column, Integer, String, DECIMAL, TIMESTAMP, JSON, MetaData, Table
from Crypto.Cipher import AES

# AES encryption helper functions
def pad(s):
    """Pad the input string to be a multiple of AES.block_size."""
    return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

def encrypt(plain_text, key):
    """Encrypt the plain_text using AES (ECB mode) with the given key."""
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plain_text)
    encrypted_bytes = cipher.encrypt(padded_text.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

# PostgreSQL connection configuration using asyncpg via SQLAlchemy
DATABASE_URL = "postgresql+asyncpg://Globetrotters:Travelvista2025@travel-vista-db.cz0agc2aa9db.us-east-1.rds.amazonaws.com:5432/travel-vista-db"
# AES key: use a 16-byte key for AES-128 (store this securely, e.g., in an environment variable)
aes_key = b'Travelvistakey'  # Replace with your secure key

# Create an async engine and sessionmaker
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Define metadata and tables using SQLAlchemy
metadata = MetaData()

# Destinations table with sensitive field 'name' to be encrypted
destinations_table = Table(
    "Destinations", metadata,
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

# User Preferences table
user_preferences_table = Table(
    "User_Preferences", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("preferences", JSON),
    Column("last_updated", TIMESTAMP),
)

# Visit Counts table
visit_counts_table = Table(
    "Visit_Counts", metadata,
    Column("visit_id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("destination_id", Integer),
    Column("visit_timestamp", TIMESTAMP),
    Column("region", String(100)),
    Column("number_of_persons", Integer),
    Column("total_price", DECIMAL),
)

# Reviews table
reviews_table = Table(
    "Reviews", metadata,
    Column("review_id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("destination_id", Integer),
    Column("rating", Integer),
    Column("review_text", String(1000)),
    Column("review_timestamp", TIMESTAMP),
)

# Activity Logs table
activity_logs_table = Table(
    "Activity_Logs", metadata,
    Column("log_id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("activity_type", String(50)),
    Column("destination_id", Integer, nullable=True),
    Column("activity_timestamp", TIMESTAMP),
    Column("additional_data", JSON),
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def insert_destinations():
    async with async_session() as session:
        with open('destinations.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Encrypt the 'name' field before inserting it
                encrypted_name = encrypt(row['name'], aes_key)
                stmt = text("""
                INSERT INTO "Destinations" (destination_id, name, world_wonder, package_option, base_price, discount_percentage, transport_modes, dynamic_tags, created_at)
                VALUES (:destination_id, :name, :world_wonder, :package_option, :base_price, :discount_percentage, :transport_modes, :dynamic_tags, :created_at)
                ON CONFLICT (destination_id) DO NOTHING;
                """)
                params = {
                    "destination_id": int(row['destination_id']),
                    "name": encrypted_name,
                    "world_wonder": row['world_wonder'],
                    "package_option": row['package_option'],
                    "base_price": float(row['base_price']),
                    "discount_percentage": int(row['discount_percentage']),
                    "transport_modes": row['transport_modes'],
                    "dynamic_tags": row['dynamic_tags'],
                    "created_at": row['created_at']
                }
                await session.execute(stmt, params)
            await session.commit()
        print("Data inserted into Destinations table.")

async def insert_user_preferences():
    async with async_session() as session:
        with open('user_preferences.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stmt = text("""
                INSERT INTO "User_Preferences" (user_id, preferences, last_updated)
                VALUES (:user_id, :preferences, :last_updated)
                ON CONFLICT (user_id) DO NOTHING;
                """)
                params = {
                    "user_id": int(row['user_id']),
                    "preferences": row['preferences'],
                    "last_updated": row['last_updated']
                }
                await session.execute(stmt, params)
            await session.commit()
        print("Data inserted into User_Preferences table.")

async def insert_visit_counts():
    async with async_session() as session:
        with open('visit_counts.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stmt = text("""
                INSERT INTO "Visit_Counts" (visit_id, user_id, destination_id, visit_timestamp, region, number_of_persons, total_price)
                VALUES (:visit_id, :user_id, :destination_id, :visit_timestamp, :region, :number_of_persons, :total_price)
                ON CONFLICT (visit_id) DO NOTHING;
                """)
                params = {
                    "visit_id": int(row['visit_id']),
                    "user_id": int(row['user_id']),
                    "destination_id": int(row['destination_id']),
                    "visit_timestamp": row['visit_timestamp'],
                    "region": row['region'],
                    "number_of_persons": int(row['number_of_persons']),
                    "total_price": float(row['total_price'])
                }
                await session.execute(stmt, params)
            await session.commit()
        print("Data inserted into Visit_Counts table.")

async def insert_reviews():
    async with async_session() as session:
        with open('reviews.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stmt = text("""
                INSERT INTO "Reviews" (review_id, user_id, destination_id, rating, review_text, review_timestamp)
                VALUES (:review_id, :user_id, :destination_id, :rating, :review_text, :review_timestamp)
                ON CONFLICT (review_id) DO NOTHING;
                """)
                params = {
                    "review_id": int(row['review_id']),
                    "user_id": int(row['user_id']),
                    "destination_id": int(row['destination_id']),
                    "rating": int(row['rating']),
                    "review_text": row['review_text'],
                    "review_timestamp": row['review_timestamp']
                }
                await session.execute(stmt, params)
            await session.commit()
        print("Data inserted into Reviews table.")

async def insert_activity_logs():
    async with async_session() as session:
        with open('activity_logs.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stmt = text("""
                INSERT INTO "Activity_Logs" (log_id, user_id, activity_type, destination_id, activity_timestamp, additional_data)
                VALUES (:log_id, :user_id, :activity_type, :destination_id, :activity_timestamp, :additional_data)
                ON CONFLICT (log_id) DO NOTHING;
                """)
                params = {
                    "log_id": int(row['log_id']),
                    "user_id": int(row['user_id']),
                    "activity_type": row['activity_type'],
                    "destination_id": row['destination_id'] if row['destination_id'] not in [None, '', 'null'] else None,
                    "activity_timestamp": row['activity_timestamp'],
                    "additional_data": row['additional_data']
                }
                await session.execute(stmt, params)
            await session.commit()
        print("Data inserted into Activity_Logs table.")

async def main():
    await create_tables()
    await insert_destinations()
    await insert_user_preferences()
    await insert_visit_counts()
    await insert_reviews()
    await insert_activity_logs()
    # Repeat similar steps for Visit_Counts, Reviews, Activity_Logs as needed

if __name__ == '__main__':
    asyncio.run(main())
