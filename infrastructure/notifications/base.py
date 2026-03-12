NOTIFICATION_REGISTRY = {}


class NotificationMeta(type):
    def __init__(cls, name, bases, attrs):
        if name != 'BaseNotification':
            NOTIFICATION_REGISTRY[name] = cls

        super().__init__(name, bases, attrs)


class BaseNotification(metaclass=NotificationMeta):
    def build_message(self, appointment_date):
        raise NotImplementedError
    
    def build_message_cancel(self, patient_id, appointment_date):
        raise NotImplementedError