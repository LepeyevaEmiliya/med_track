from abc import ABC, abstractmethod


class BaseUser(ABC):
    def __init__(self, id, name, email, role, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.created_at = created_at


    @abstractmethod
    def get_permissions(self) -> list[str]:
        pass


class Patient(BaseUser):
    def __init__(self, id, name, email, role, created_at, birth_date):
        self.birth_date = birth_date
        super().__init__(id, name, email, role, created_at)


    def get_permissions(self):
        return ['read_own_records', 'create_appointment']


class Doctor(BaseUser):
    def __init__(self, id, name, email, role, created_at, specialization):
        self.specialization = specialization
        super().__init__(id, name, email, role, created_at)


    def get_permissions(self):
        return ['read_patient_records', 'create_appointment', 'update_prescription']
