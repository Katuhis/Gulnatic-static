from bson import ObjectId
from datetime import datetime
from pymongo import collection, errors
from typing import Dict, List

from db import db
from common.exceptions import MainError


class VersionModel:
    _collection: collection
    _id: ObjectId
    number: int
    date_upload: datetime
    status: bool

    def __init__(self,
                 number: int,
                 date_upload: datetime = None,
                 status: bool = None) -> None:
        self._collection = db.db["versions"]
        self.number = number
        self.date_upload = date_upload
        self.status = status
        self._search = {}
        if self.number:
            self._search["number"] = self.number
        if self.date_upload:
            self._search["dateUpload"] = self.date_upload
        if self.status:
            self._search["status"] = self.status

    def find(self) -> Dict:
        try:
            return self._collection.find_one(self._search)
        except errors.PyMongoError as pymongo_error:
            raise MainError(500100, str(pymongo_error))

    def insert(self) -> ObjectId:
        try:
            return self._collection.insert_one({
                "number": self.number,
                "dateUpload": self.date_upload,
                "status": self.status
            }).inserted_id
        except errors.PyMongoError as pymongo_error:
            raise MainError(500100, str(pymongo_error))


class VersionListModel:
    _collection: collection
    _data: List[Dict]

    def __init__(self, data: List[Dict] = None, search: Dict = None, sort: List = None) -> None:
        self._collection = db.db["versions"]
        self._data = data
        self._search = search
        self._sort = sort

    def find(self) -> List[Dict]:
        try:
            result = list(self._collection.find(self._search).sort(self._sort))

            self._data = [
                {
                    "number": r['number'],
                    "dateUpload": r['dateUpload'],
                    "status": r['status']
                }
                for r in result
            ]

            return self._data
        except errors.PyMongoError as pymongo_error:
            raise MainError(500100, str(pymongo_error))

    def insert(self) -> List[Dict]:
        try:
            result_ids = self._collection.insert_many(self._data).inserted_ids

            return self._collection.find({"_id": {"$in": result_ids}}).sort([("_id", -1)])
        except errors.PyMongoError as pymongo_error:
            raise MainError(500100, str(pymongo_error))
