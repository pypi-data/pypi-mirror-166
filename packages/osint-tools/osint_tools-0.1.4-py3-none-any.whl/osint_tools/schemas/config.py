from .base import *
from datetime import datetime

datetime_to_date = lambda t: t.isoformat(' ', 'hours').split(' ')[0]
datetime_to_str = lambda t: t.isoformat()
datetime_to_unix_epoch = lambda x: x.timestamp()


class BaseConfig(BaseModel):

    def to_dict(self, **kwargs):
        # print(kwargs)
        data = self.dict(by_alias=True)
        # print(data)
        data["_id"] = str(self.id)
        return data

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            # datetime: datetime_to_unix_epoch
            datetime: datetime_to_str
        }

class CreateConfig(BaseModel):

    def to_dict(self, **kwargs):
        data = self.dict(by_alias=True)
        data["_id"] = str(self.id)
        return data

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # json_encoders = {
            # bson.decimal128.Decimal128: lambda x: x.to_decimal(),
            # bson.decimal128.Decimal128: lambda x: str(x),
        # }


class CreateExpenseConfig(BaseModel):
    
    def to_dict(self, **kwargs):
        # print(kwargs)
        data = self.dict(by_alias=True)
        # print(data)
        data["_id"] = str(self.id)
        return data

    # def to_mongo(self, **kwargs):
    #     exclude_unset = kwargs.pop('exclude_unset', True)
    #     by_alias = kwargs.pop('by_alias', True)
    #     parsed = self.dict(exclude_unset=exclude_unset, by_alias=by_alias, **kwargs)
    #     # Mongo uses `_id` as default key.
    #     if '_id' not in parsed and 'id' in parsed:
    #         parsed['_id'] = parsed.pop('id')
    #     return parsed

    # @classmethod
    # def from_mongo(cls, data: dict):
    #     """Convert _id into "id". """
    #     if not data:
    #         return data
    #     id = data.pop('_id', None)
    #     return cls(**dict(data, id=id))


    class Config:
        anystr_strip_whitespace = True# same as str.strip()
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            # UUID: lambda x: str(x)
            # datetime: datetime_to_unix_epoch
            # datetime: datetime_to_str
        }

        schema_extra = {
            "Type": {
                "Text": "VENDOR_NAME",
                "Confidence": 92.35983276367188
            },
            "LabelDetection": {
                "Text": "Your account number/Votre num\u00e9ro de compte",
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.26004040241241455,
                        "Height": 0.011014322750270367,
                        "Left": 0.6431170701980591,
                        "Top": 0.7729629874229431
                    },
                    "Polygon": [
                        {
                            "X": 0.6431170701980591,
                            "Y": 0.7729629874229431
                        },
                        {
                            "X": 0.9031574726104736,
                            "Y": 0.7729629874229431
                        },
                        {
                            "X": 0.9031574726104736,
                            "Y": 0.7839772701263428
                        },
                        {
                            "X": 0.6431170701980591,
                            "Y": 0.7839772701263428
                        }
                    ]
                },
                "Confidence": 54.14602279663086
            },
            "PageNumber": 1
        }



# class AnalyzeDocConfig(BaseModel):
#     class Config:
#         # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.detect_document_text
#         anystr_strip_whitespace = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         schema_extra = {
#         {
#             'DocumentMetadata': {
#                 'Pages': 123
#             },
#             'Blocks': [
#                 {
#                     'BlockType': "'KEY_VALUE_SET'|'PAGE'|'LINE'|'WORD'|'TABLE'|'CELL'|'SELECTION_ELEMENT'|'MERGED_CELL'|'TITLE'|'QUERY'|'QUERY_RESULT'",
#                     'Confidence': ...,
#                     'Text': 'string',
#                 'TextType': "'HANDWRITING'|'PRINTED'",
#                     'RowIndex': 123,
#                     'ColumnIndex': 123,
#                     'RowSpan': 123,
#                     'ColumnSpan': 123,
#                     'Geometry': {
#                         'BoundingBox': {
#                             'Width': ...,
#                             'Height': ...,
#                             'Left': ...,
#                             'Top': ...
#                         },
#                         'Polygon': [
#                             {
#                                 'X': ...,
#                                 'Y': ...
#                             },
#                         ]
#                     },
#                     'Id': 'string',
#                     'Relationships': [
#                         {
#                             'Type': 'VALUE'|'CHILD'|'COMPLEX_FEATURES'|'MERGED_CELL'|'TITLE'|'ANSWER',
#                             'Ids': [
#                                 'string',
#                             ]
#                         },
#                     ],
#                     'EntityTypes': [
#                         'KEY'|'VALUE'|'COLUMN_HEADER',
#                     ],
#                     'SelectionStatus': 'SELECTED'|'NOT_SELECTED',
#                     'Page': 123,
#                     'Query': {
#                         'Text': 'string',
#                         'Alias': 'string',
#                         'Pages': [
#                             'string',
#                         ]
#                     }
#                 },
#             ],
#             'DetectDocumentTextModelVersion': 'string'
#         }
#     }
