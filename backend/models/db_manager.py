import json
import shutil
import threading
from pathlib import Path
from backend.config import Config

_lock = threading.Lock()

class DatabaseManager:
    _instance = None
    _data = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseManager()
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        with _lock:
            active_path = Config.PERSISTENT_DATA_PATH
            sample_path = Config.SAMPLE_DATA_PATH

            if not active_path.exists():
                active_path.parent.mkdir(parents=True, exist_ok=True)
                if sample_path.exists():
                    shutil.copyfile(sample_path, active_path)
                else:
                    empty_db = {
                        "users": [],
                        "hotels": [],
                        "rooms": [],
                        "bookings": [],
                        "payments": []
                    }
                    with open(active_path, "w", encoding="utf-8") as f:
                        json.dump(empty_db, f, indent=2)

            with open(active_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def _reload_if_needed(self):
        active_path = Config.PERSISTENT_DATA_PATH
        if active_path.exists():
            try:
                mtime = active_path.stat().st_mtime
                if not hasattr(self, '_last_mtime') or mtime > self._last_mtime:
                    with open(active_path, "r", encoding="utf-8") as f:
                        self._data = json.load(f)
                    self._last_mtime = mtime
            except Exception:
                pass

    def get_all(self, collection_name: str) -> list[dict]:
        with _lock:
            self._reload_if_needed()
            return list(self._data.get(collection_name, []))

    def find_one(self, collection_name: str, query: dict) -> dict | None:
        with _lock:
            self._reload_if_needed()
            items = self._data.get(collection_name, [])
            for item in items:
                match = all(item.get(k) == v for k, v in query.items())
                if match:
                    return dict(item)
            return None

    def find(self, collection_name: str, query: dict | None = None) -> list[dict]:
        with _lock:
            self._reload_if_needed()
            items = self._data.get(collection_name, [])
            if not query:
                return [dict(i) for i in items]
            result = []
            for item in items:
                match = all(item.get(k) == v for k, v in query.items())
                if match:
                    result.append(dict(item))
            return result

    def insert(self, collection_name: str, doc: dict) -> dict:
        with _lock:
            if collection_name not in self._data:
                self._data[collection_name] = []
            self._data[collection_name].append(doc)
            self._save()
            return dict(doc)

    def update(self, collection_name: str, query: dict, update_fields: dict) -> dict | None:
        with _lock:
            items = self._data.get(collection_name, [])
            for item in items:
                match = all(item.get(k) == v for k, v in query.items())
                if match:
                    item.update(update_fields)
                    self._save()
                    return dict(item)
            return None

    def delete(self, collection_name: str, query: dict) -> bool:
        with _lock:
            items = self._data.get(collection_name, [])
            initial_len = len(items)
            self._data[collection_name] = [
                item for item in items if not all(item.get(k) == v for k, v in query.items())
            ]
            if len(self._data[collection_name]) != initial_len:
                self._save()
                return True
            return False

    def _save(self):
        Config.PERSISTENT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(Config.PERSISTENT_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)
        self._sync_to_mongodb()

    def _sync_to_mongodb(self):
        try:
            from pymongo import MongoClient
            client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=800)
            mongo_db = client["hotel_booking_db"]
            for col_name in ["users", "hotels", "rooms", "bookings", "payments"]:
                items = self._data.get(col_name, [])
                col = mongo_db[col_name]
                col.delete_many({})
                if items:
                    docs = []
                    for item in items:
                        doc = dict(item)
                        if "id" in doc:
                            doc["_id"] = doc["id"]
                        docs.append(doc)
                    col.insert_many(docs)
        except Exception:
            pass

db = DatabaseManager.get_instance()
