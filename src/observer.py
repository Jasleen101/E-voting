from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class LoggingSystem(Observer):
    def update(self):
        print("Election conducted. Logging system updated.")
