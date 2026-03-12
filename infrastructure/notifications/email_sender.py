from .base import BaseNotification
from domain.interfaces import INotificationSender


class EmailNotification(BaseNotification):
    def build_message(self, appointment_date):
        message = f'You have an appointment on {appointment_date}'
        return message
    
    def build_message_cancel(self, patient_id, appointment_date):
        message = f'Patient {patient_id} has cancelled an appointment on {appointment_date}'
        return message
    

class EmailNotificationSender(INotificationSender):
    def send(self, recipient, message):
        print(f'Sending email to {recipient}: {message}')