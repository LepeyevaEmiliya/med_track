# Базовый класс для исключений
class MedTrackError(Exception):
    pass


# Исключение для случаев, когда пациент не найден
class PatientNotFoundError(MedTrackError):
    def __init__(self, patient_id):
        self.patient_id = patient_id
        super().__init__(f"Patient {patient_id} is not found")


# Исключение для случаев, когда дозировка указана некорректно
class InvalidDosageError(MedTrackError):
    def __init__(self, dosage):
        self.dosage = dosage
        super().__init__(f"Invalid dosage form error: {dosage}")


# Исключение для случаев, когда пытаются записать на время, когда врач уже занят
class AppointmentConflictError(MedTrackError):
    def __init__(self, doctor_id, time):
        self.doctor_id = doctor_id
        self.time = time
        super().__init__(f"Doctor {doctor_id} has a conflicting appointment at {time}")


# Исключение для случаев, когда пытаются войти в систему, куда пользователю нет доступа
class UnauthorizedAccessError(MedTrackError):
    def __init__(self, required_role):
        self.required_role = required_role
        super().__init__(f"The role {required_role} is required")