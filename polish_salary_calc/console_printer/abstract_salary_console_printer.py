from abc import ABC,abstractmethod
from dataclasses import dataclass


@dataclass
class AbstractSalaryConsolePrinter[T](ABC):
    contract: T

    @abstractmethod
    def print_rates(self) -> str:
        pass

    @abstractmethod
    def print_options(self) -> str:
        pass

    @abstractmethod
    def print_contract(self) -> str:
        pass

    @abstractmethod
    def print_all(self) -> str:
        pass

