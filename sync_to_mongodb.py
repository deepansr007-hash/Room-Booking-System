import json
from pathlib import Path
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "database" / "active_database.json"

def sync_active_data_to_mongodb():
    print("Connecting to MongoDB at mongodb://localhost:27017/ ...")
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    
    # Verify connection
    client.admin.command('ping')
    print("[SUCCESS] Successfully connected to MongoDB Server!")

    db_name = "hotel_booking_db"
    db = client[db_name]

    if not DB_FILE.exists():
        print(f"[ERROR] Database file not found at: {DB_FILE}")
        return

    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    collections = ["users", "hotels", "rooms", "bookings", "payments"]

    for col_name in collections:
        items = data.get(col_name, [])
        col = db[col_name]
        col.delete_many({}) # Clear existing to maintain exact mirror
        
        if items:
            # Prepare documents (MongoDB uses _id as primary key, preserve original id)
            docs = []
            for item in items:
                doc = dict(item)
                # Map or keep id and _id
                if "id" in doc:
                    doc["_id"] = doc["id"]
                docs.append(doc)
            col.insert_many(docs)
            print(f" -> Synced {len(docs)} documents into collection '{col_name}' in database '{db_name}'.")
        else:
            print(f" -> Collection '{col_name}' has 0 records.")

    print("\n========================================================")
    print(f"  All collections successfully synced into MongoDB database: '{db_name}'!")
    print("========================================================")

if __name__ == "__main__":
    sync_active_data_to_mongodb()
