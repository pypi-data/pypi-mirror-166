from typing import Any

from pymongo import MongoClient

from ampel.abstract.AbsAlertLoader import AbsAlertLoader
from ampel.abstract.AbsOpsUnit import AbsOpsUnit
from ampel.model.UnitModel import UnitModel
from ampel.base.AuxUnitRegister import AuxUnitRegister

class MongoAlertArchiver(AbsOpsUnit):

    loader: UnitModel

    database: str
    collection: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.alert_loader: AbsAlertLoader[dict] = AuxUnitRegister.new_unit(
            model=self.loader, sub_type=AbsAlertLoader
        )

        self._collection = (
            MongoClient(self.context.db.mongo_uri)
            .get_database(self.database)
            .get_collection(self.collection)
        )
    
    def run(self, beacon: None | dict[str, Any] = None) -> None | dict[str, Any]:
        return super().run(beacon)

        # self.context.db.
