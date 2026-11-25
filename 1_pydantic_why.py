from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Dict,List,Optional,Annotated 

class patient(BaseModel):
    name: Annotated[str, Field(..., description = "Enter the Pateient name", example = ["Vijay", "Vinay"])]
    age: int
    state: str
    height: float
    weight: float
    married: Optional[bool] = None
    contact: Dict[str, str]
    allergies: List[str]

@field_validator("age")
@classmethod
def age_validate(cls,value):
    if value <2 :
        raise ValueError("Age should be greater than 2")
    return value


patient_info={"name":"Vamshi", "age":30, "state":"Telangana", "height":5.8, "weight":70.5, "married":True, "contact":{"email":"vamshi@example.com"}, "allergies":["Peanuts"]}
patient1=patient(**patient_info)


def insert_patient_info(patient_info:patient):
    print(patient1.name)
    print(patient1.age)
    print("Inserted")

insert_patient_info(patient1)