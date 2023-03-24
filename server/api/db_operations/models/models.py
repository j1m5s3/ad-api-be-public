import uuid
import datetime
from typing import Optional
from pydantic import BaseModel, Field, PrivateAttr


class User(BaseModel):
    user_name: str = Field(...)
    email_address: str = Field(...)
    password: str = Field(..., max_length=25)
    is_space_provider: bool = Field(...)
    is_advertisement_provider: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        """
        json_encoders = {
            datetime.datetime.now(): lambda v: v.__str__(),
            uuid.UUID: lambda v: v.__str__(),
        }
        """


class UserUpdater(BaseModel):
    user_name: Optional[str]
    updated_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="updatedAt")
    email_address: Optional[str]
    is_space_provider: Optional[bool]
    is_advertisement_provider: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "user_name": "j1m5s3",
                "email_address": "jj@gmail.com",
                "is_space_provider": True,
                "is_advertisement_provider": True
            }
        }


class Space(BaseModel):
    _space_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="createdAt")
    updated_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="updatedAt")
    is_space_ad_populated: bool = Field(...)
    space_provider_id: str = Field(...)

    ref_space_contract_id: str = Field(...)
    ref_ad_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "d0ec9914-20aa-4023-9060-54626c02c463",
                "is_space_ad_populated": False,
                "space_provider_id": "c8cf8453-965c-4a10-b2f9-fb618dbd2834",
                "ref_space_contract_id": "fa937ac6-3c86-45bb-a2ab-e39a75b29515",
                "ref_ad_id": None
            }
        }


class SpaceUpdater(BaseModel):
    is_space_ad_populated: Optional[bool]
    space_provider_id: Optional[str]
    created_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="createdAt")
    updated_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="updatedAt")
    ref_space_contract_id: Optional[str]
    ref_ad_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "_id": "d0ec9914-20aa-4023-9060-54626c02c463",
                "is_space_ad_populated": True,
                "space_provider_id": "c8cf8453-965c-4a10-b2f9-fb618dbd2834",
                "ref_space_contract_id": "fa937ac6-3c86-45bb-a2ab-e39a75b29515",
                "ref_ad_id": "faa20ba9-db4f-45be-a838-683c94738126"
            }
        }


class Advertisement(BaseModel):
    _ad_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    advertisement_provider_id: str = Field(...)
    created_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="createdAt")

    ref_advertisement_contract_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "390f5c48-d203-4000-8e37-21bd1e86a24b",
                "advertisement_provider_id": "390f5c48-d203-4000-8e37-21bd1e86a24b",
                "ref_advertisement_contract_id": "312c7027-6d0c-40cf-84af-5566fa66ef91",
            }
        }


class Auction(BaseModel):
    unique_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    is_complete: bool = Field(...)
    created_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="createdAt")
    updated_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="updatedAt")
    ref_auction_contract_id: str = Field(...)
    ref_data: dict = Field(...)
    ref_provider_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "65105305-d14f-4381-8c10-cb7fe474c234",
                "ref_auction_contract_id": "91510e6d-4330-478e-aecd-d07b68d787ff",
                "ref_provider_id": "c8cf8453-965c-4a10-b2f9-fb618dbd2834",
            }
        }


class AuctionUpdater(BaseModel):
    is_complete: Optional[bool] = Field(...)
    updated_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="updatedAt")
    ref_auction_contract_id: Optional[str] = Field(...)
    ref_auctioned_contract_id: Optional[str] = Field(...)
    ref_provider_id: str = Field(...)


class Contracts(BaseModel):
    unique_id: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_at: Optional[str] = Field(default_factory=datetime.datetime.now, alias="createdAt")
    contract_address: str = Field(...)
    token_id: Optional[int] = Field(default=None)
    contract_type: str = Field(...)  # space, advertisement, space_auction, advertisement_auction
    contract_standard: Optional[str] = Field(default=None)  # erc721, erc1155

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "advertisement": {
                "_id": "312c7027-6d0c-40cf-84af-5566fa66ef91",
                "contract_address": "0xDC45B05560DB8982401263b41D93cE4A175001f9",
                "token_id": "80712783243573046485554901753729909091141402880130508043030777510837285289985",
                "contract_type": "advertisement",
                "contract_standard": "erc721"
            },
            "space": {
                "_id": "fa937ac6-3c86-45bb-a2ab-e39a75b29515",
                "contract_address": "0x46C5b72edeef03Cec5eBA043F2070C4FbaE9f63A",
                "token_id": "0",
                "contract_type": "space",
                "contract_standard": "erc721"
            }
        }
