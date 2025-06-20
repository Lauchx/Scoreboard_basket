from abc import ABC, abstractmethod

class Time(ABC):
    @abstractmethod
    def reset_time():
        pass
    @abstractmethod()
    def initialization_time():
        pass
    @abstractmethod()
    def stop_time():
        pass