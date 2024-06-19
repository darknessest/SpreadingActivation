from enum import IntEnum

class SchemaType(IntEnum):
    partnership = 1
    feature = 2
    value_prop = 3
    customer_seg = 4
    channel = 5
    market = 6
    # adjust the schema type as needed

    # get last element
    @classmethod
    def last(cls):
        return list(cls)[-1]
    
    # get first element
    @classmethod
    def first(cls):
        return list(cls)[0]