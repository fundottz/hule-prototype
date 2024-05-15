from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, Union

class PersonalDetails(BaseModel):
    fullname: str = Field(
        default="",
        description="The full name of the user.",
    )
    gender: str = Field(
        default="",
        enum=["male", "female"], description="This is the gender of the user.",
    )
    age: int = Field(
        default=0,
        description="This is the age for the user required to filter the plans based on age.",
    )
    city: str = Field(
        default="",
        description="The name of the city where someone lives",
    )
    global_coverage_need: Optional[Union[bool, None]] = Field(
        None,
        description="Does the user need global coverage?",
    )
    visa_coverage_need: Optional[Union[bool, None]] = Field(
        None,
        description="Does the user need visa coverage?"
    )