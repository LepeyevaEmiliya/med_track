from dataclasses import dataclass
from datetime import date, datetime

@dataclass(frozen=True)
class UserDTO:
    id: int | None
    name: str
    email: str
    role: str
    created_at: datetime | None


@dataclass(frozen=True)
class PatientDTO:
    id: int | None
    user_id: int
    birth_date: date


@dataclass(frozen=True)
class DoctorDTO:
    id: int | None
    user_id: int
    specialization: str

    def __post_init__(self):
        key = 'specialization'
        field = getattr(self, key)
        if field.strip()  == '':
            raise ValueError(f'{key} must be filled')


@dataclass(frozen=True)
class AppointmentDTO:
    id: int | None
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: str | None


@dataclass(frozen=True)
class MeasurementDTO:
    id: int | None
    patient_id: int
    systolic_pressure: float
    diastolic_pressure: float
    glucose_level: float
    measured_at: datetime | None

    def __post_init__(self):
        date_today = datetime.now()
        if self.measured_at is not None and self.measured_at > date_today:
            raise ValueError(f'The measurement date must be today({date_today}) or earlier')
        
        measures = (
            'systolic_pressure',
            'diastolic_pressure',
            'glucose_level',
            )

        for key in measures:
            measure = getattr(self, key)
            if not isinstance(measure, float):
                raise ValueError(f'{key} must be float')
            elif measure <= 0:
                raise ValueError(f'{key} must be greater than 0')


@dataclass(frozen=True)
class PrescriptionDTO:
    id: int | None
    patient_id: int 
    doctor_id: int
    complaints: str | None
    medication: str

    def __post_init__(self):
        key = 'medication'
        field = getattr(self, key)
        if field.strip()  == '':
            raise ValueError(f'{key} must be filled')
            
        object.__setattr__(self, key, field.strip())
            

            
