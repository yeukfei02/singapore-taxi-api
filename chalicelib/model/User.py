from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model
from datetime import datetime


class UserModel(Model):
    class Meta:
        table_name = "SingaporeTaxiApiUser"
        region = "ap-southeast-1"
        host = "https://dynamodb.ap-southeast-1.amazonaws.com"
    id = UnicodeAttribute(hash_key=True, null=False)
    email = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False, default=datetime.now())

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(UserModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))


if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1)
