from typing import Any, List, Optional

from classifier_model.processing.validation import PatientDataInputSchema
from pydantic import BaseModel


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[int]]


class MultiplePatientDataInputs(BaseModel):
    inputs: List[PatientDataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "Age": 63,
                        "Sex": "F",
                        "ChestPainType": "ATA",
                        "RestingBP": 140,
                        "Cholesterol": 195,
                        "FastingBS": 0,
                        "RestingECG": "Normal",
                        "MaxHR": 179,
                        "ExerciseAngina": "N",
                        "Oldpeak": 0.0,
                        "ST_Slope": "Up"
                    }
                ]
            }
        }
