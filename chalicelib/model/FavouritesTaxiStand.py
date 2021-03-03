from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.models import Model
from datetime import datetime


class FavouritesTaxiStandModel(Model):
    class Meta:
        table_name = "SingaporeTaxiApiFavouritesTaxiStand"
        region = "ap-southeast-1"
        host = "https://dynamodb.ap-southeast-1.amazonaws.com"
    id = UnicodeAttribute(hash_key=True, null=False)
    taxiCode = UnicodeAttribute(null=False)
    latitude = NumberAttribute(null=False, default=0)
    longitude = NumberAttribute(null=False, default=0)
    bfa = UnicodeAttribute(null=False)
    ownership = UnicodeAttribute(null=False)
    type = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    userId = UnicodeAttribute(null=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False, default=datetime.now())

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(FavouritesTaxiStandModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))


if not FavouritesTaxiStandModel.exists():
    FavouritesTaxiStandModel.create_table(
        read_capacity_units=1, write_capacity_units=1)
