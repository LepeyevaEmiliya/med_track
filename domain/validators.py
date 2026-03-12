from dataclasses import dataclass
from datetime import date
from .exceptions import InvalidDosageError
from .decorators import log_call

@dataclass
class BloodPressure:
    systolic: int
    diastolic: int


@dataclass
class Dosage:
    amount: int
    unit: str


@log_call
def validate_blood_pressure(value: str) -> BloodPressure:
    pressure = value.split('/')
    try:
        systolic = int(pressure[0])
        diastolic = int(pressure[1])
    except (ValueError, IndexError) as e:
        raise ValueError('Pressure form is incorrect') from e
    else:
        if not 60 <= systolic <= 250:
            raise ValueError('Systolic pressure is incorrect')
        elif not 40 <= diastolic <= 150:
            raise ValueError('Diastolic pressure is incorrect')
        elif systolic <= diastolic:
            raise ValueError('Diastolic pressure can not be more than systolic')

        return BloodPressure(systolic, diastolic)


@log_call
def validate_dosage(value: str) -> Dosage:
    allowed_units = {"mg", "ml", "mcg", "tablet", "capsule"}
    dosage = value.split(' ')
    try:
        amount = int(dosage[0])
        unit = dosage[1].lower()
    except (ValueError, IndexError) as e:
        raise ValueError('Dosage form is incorrect') from e
    else:
        if unit not in allowed_units:
            raise InvalidDosageError('Unit should be one of these: "mg", "ml", "mcg", "tablet", "capsule"')
        elif amount <= 0:
            raise InvalidDosageError('Dosage is incorrect')

        return Dosage(amount, unit)


@log_call
def validate_date(appointment: date) -> date:
    today_date = date.today()
    if appointment < today_date:
        raise ValueError(f'Appointment date {appointment} should be more than {today_date}')

    return appointment
