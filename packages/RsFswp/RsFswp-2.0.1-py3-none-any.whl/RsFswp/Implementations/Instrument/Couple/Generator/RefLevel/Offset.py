from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, level: float) -> None:
		"""SCPI: INSTrument:COUPle:GENerator:RLEVel:OFFSet \n
		Snippet: driver.instrument.couple.generator.refLevel.offset.set(level = 1.0) \n
		No command help available \n
			:param level: No help available
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'INSTrument:COUPle:GENerator:RLEVel:OFFSet {param}')

	def get(self) -> float:
		"""SCPI: INSTrument:COUPle:GENerator:RLEVel:OFFSet \n
		Snippet: value: float = driver.instrument.couple.generator.refLevel.offset.get() \n
		No command help available \n
			:return: level: No help available"""
		response = self._core.io.query_str(f'INSTrument:COUPle:GENerator:RLEVel:OFFSet?')
		return Conversions.str_to_float(response)
