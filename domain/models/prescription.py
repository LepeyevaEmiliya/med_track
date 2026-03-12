class Prescription:
    def __init__(self, id, patient_id, doctor_id, complaints, medication):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.complaints = complaints
        self.medication = medication