from .models import VPS


def get_record_set(x):
    resource_records = list(map(lambda y: y.get("Value"), x.get("ResourceRecords", [])))
    record = {
        "name": x.get("Name"),
        "record_type": x.get("Type"),
        "resource": resource_records,
    }

    return record
