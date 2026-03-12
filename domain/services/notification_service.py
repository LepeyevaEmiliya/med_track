from domain.interfaces import INotificationSender
from infrastructure.notifications.base import NOTIFICATION_REGISTRY


class NotificationService:
    def __init__(self, notification_sender: INotificationSender):
        self.sender = notification_sender


    async def notify_patient_about_appointment(self, notification_type, appointment_date, recipient):
        notification_class = NOTIFICATION_REGISTRY[notification_type]
        notification = notification_class()

        message = notification.build_message(appointment_date)
        self.sender.send(recipient, message)


    async def notify_doctor_about_cancellation(self, notification_type, patient_id, appointment_date, recipient):
        notification_class = NOTIFICATION_REGISTRY[notification_type]
        notification = notification_class()

        message = notification.build_message_cancel(patient_id, appointment_date)
        self.sender.send(recipient, message)