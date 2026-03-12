class ValidateField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


    def __set__(self, instance, value):
        if isinstance(value, (int, float)):
            ranges = {
                '_systolic_pressure': (60, 250),
                '_diastolic_pressure': (40, 150),
                '_glucose_level': (3.5, 30),
            }

            min_val, max_val = ranges[self.name]
            if not min_val <= value <= max_val:
                raise ValueError(f"{self.name[1:]} is out of range")

            instance.__dict__[self.name] = value


    def __set_name__(self, owner, name):
        self.name = '_' + name


class Measurement:
    systolic_pressure = ValidateField()
    diastolic_pressure = ValidateField()
    glucose_level = ValidateField()

    def __init__(self, id, patient_id, systolic_pressure, diastolic_pressure, glucose_level, measured_at):
        self.id = id
        self.patient_id = patient_id
        self.systolic_pressure = systolic_pressure
        self.diastolic_pressure = diastolic_pressure
        self.glucose_level = glucose_level
        self.measured_at = measured_at

