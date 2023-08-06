from pymongo import MongoClient

from .data import ds_applicants, mscfe_applicants
from .experiment import Experiment


class Reset(Experiment):
    def __init__(
        self, repo=MongoClient(host="localhost", port=27017), db="wqu-abtest"
    ):
        super().__init__(repo, db=db)

    def reset_database(self):
        collections = [
            ("ds-applicants", ds_applicants),
            ("mscfe-applicants", mscfe_applicants),
        ]
        for c, data in collections:
            self.repo.drop_collection(c)
            self.repo.create_collection(c)
            self.repo.insert(c, data)
            print(f"Reset '{c}' collection. Now has {len(data)} documents.")
