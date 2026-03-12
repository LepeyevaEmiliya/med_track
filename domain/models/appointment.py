class Appointment:
    def __init__(self, id, doctor_id, patient_id, appointment_date, status):
        self.id = id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.appointment_date = appointment_date
        self.status = status