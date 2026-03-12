from abc import ABC, abstractmethod


class INotificationSender(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass