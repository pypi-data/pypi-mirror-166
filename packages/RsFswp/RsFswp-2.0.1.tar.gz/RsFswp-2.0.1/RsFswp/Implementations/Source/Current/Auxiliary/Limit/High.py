from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class High:
	"""High commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("high", core, parent)

	def set(self, current: float) -> None:
		"""SCPI: SOURce:CURRent:AUX:LIMit:HIGH \n
		Snippet: driver.source.current.auxiliary.limit.high.set(current = 1.0) \n
		This command returns the maximum current of the Vaux connector. \n
			:param current: numeric value The return value is always 0.1 A.
		"""
		param = Conversions.decimal_value_to_str(current)
		self._core.io.write(f'SOURce:CURRent:AUX:LIMit:HIGH {param}')

	def get(self) -> float:
		"""SCPI: SOURce:CURRent:AUX:LIMit:HIGH \n
		Snippet: value: float = driver.source.current.auxiliary.limit.high.get() \n
		This command returns the maximum current of the Vaux connector. \n
			:return: current: numeric value The return value is always 0.1 A."""
		response = self._core.io.query_str(f'SOURce:CURRent:AUX:LIMit:HIGH?')
		return Conversions.str_to_float(response)
