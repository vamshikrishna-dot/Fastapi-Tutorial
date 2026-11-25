from fastapi import FastAPI, Path, HTTPException,Query 
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional

class Patient(BaseModel):
    id : Annotated[str,Field(...,description="Enter the Patient ID",example="P001")]
    name: Annotated[str,Field(...,description ="Enter Patient name",example="Vijay")]
    city : Annotated[str,Field(...,description="Enter the city name",example="Hyderabad")]
    age : Annotated[int,Field(...,description="Enter the age in years",example=30,gt=0,lt=120)]
    gender : Annotated[str,Field(...,description="Enter the gender",example="Male")]
    height : Annotated[float,Field(...,description="Enter the height in meters",example=1.75)]
    weight : Annotated[float,Field(...,description="Enter the weight in kilograms",example=70.5)]

    @computed_field
    @property
    def BMI(self) -> float :
        return round(self.weight/self.height**2,2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.BMI <18.5:
            return "underweight"
        elif self.BMI <25:
            return "normal"
        elif self.BMI <30:
            return "overweight"
        else:
            return "obese"


class Update(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None)]
    gender:Annotated[Optional[str],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None)]
    weight:Annotated[Optional[float],Field(default=None)]

app= FastAPI()

def load_data():
    file = open(("patients.json"), "r")
    data = json.load(file)
    return data

def save_data(data):
    file = open("patients.json","w")
    json.dump(data,file)


@app.get("/")
def hello():
    return {"message": "Patient Management System"}

@app.get("/about")
def about():
    return {"message": "Fully functional Patient Management System built with FastAPI and Python."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id : str = Path(..., description = "Enter the Patient ID", example = "P001",min_length = 4)):
    #load data
    data = load_data()

    if patient_id in data :
        return data[patient_id]
    raise HTTPException (status_code = 404, detail = "Patient Not Found")

@app.get("/sort")
def sorted_patients(sort_by : str = Query(..., description = "Enter the height, weight or BMI"),order : str = Query("asc",description = "sort in asc or desc order")):
    data = load_data()
    check_data=["height","weight","BMI"]
    if sort_by not in check_data:
        raise HTTPException(status_code = 400, detail =f'Provide value from {check_data}')

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code = 400, detail =f'Provide value from [\"asc\", \"desc\"]')

    sorted_data = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=(order == "desc"))
    return dict(sorted_data)

@app.post("/create")
def create_patient(patient : Patient):
    # load data
    data = load_data()
    
    #check ifpatient already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient already exists")

    # add patient to the database
    data[patient.id] = patient.model_dump(exclude = ['id'])
    # save the file
    save_data(data)
    #json response
    return JSONResponse(status_code=201,content="Patient addded Succesfully")

@app.put("/edit/{patient_id}")
def update_patient(patient_id : str,patient_update : Update):
    #Load data 
    data = load_data()
    # Check if the patient id exists in the database
    if patient_id not in data:
        raise HTTPException(status_code=400,detail=("patient does not exist"))

    # put the patient needed to updated into a variable with pat id
    existing_patient_info = data[patient_id]
    #put the info for update in a variable and convert to python dict
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    #create a loop where the updating patient values edits the existing data
    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value
        
        data[patient_id]=existing_patient_info
        #save the data into database
        save_data(data)

        
        return JSONResponse(status_code=200,content={'message':'update successful'})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    #load data
    data=load_data()
    #check if patient is in the DB
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient do not exist")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content="Patient deleted successfully")
      



    