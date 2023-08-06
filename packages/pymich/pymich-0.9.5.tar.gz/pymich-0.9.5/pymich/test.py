import functools
from pathlib import Path
import os

from pymich.compiler import Compiler
from pytezos import ContractInterface


class ContractLoader:
    """
    This object provides a Python API over example contracts, for testing.
    """

    def __init__(self, contract_path):
        self.contract_path = contract_path

    @functools.cached_property
    def source(self):
        with open(self.contract_path) as f:
            return f.read()

    @functools.cached_property
    def compiler(self):
        return Compiler(self.source)

    @functools.cached_property
    def micheline(self):
        return self.compiler.compile_contract()

    @functools.cached_property
    def interface(self):
        return ContractInterface.from_micheline(self.micheline)

    @property
    def dummy(self):
        return self.interface.storage.dummy()

    @property
    def storage(self):
        """ Lazy mutable storage, dummy by default. """
        if '_storage' not in self.__dict__:
            self._storage = self.dummy
        return self._storage

    @storage.setter
    def storage(self, value):
        self._storage = value

    @classmethod
    def factory(cls, path):
        pymich = Path(os.path.dirname(__file__)) / '..'
        paths = [
            Path(path),
            pymich / 'tests' / path,
            pymich / 'tests' / 'end_to_end' / path,
        ]
        for path in paths:
            if path.exists():
                return cls(path.absolute())
