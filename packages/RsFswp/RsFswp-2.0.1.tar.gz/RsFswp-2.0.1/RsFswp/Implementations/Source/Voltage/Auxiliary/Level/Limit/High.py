from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class High:
	"""High commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("high", core, parent)

	def set(self, voltage: float) -> None:
		"""SCPI: SOURce:VOLTage:AUX:LEVel:LIMit:HIGH \n
		Snippet: driver.source.voltage.auxiliary.level.limit.high.set(voltage = 1.0) \n
		This command defines the maximum voltage that may be supplied by the Vaux source. \n
			:param voltage: numeric value Range: -10 to 10, Unit: V
		"""
		param = Conversions.decimal_value_to_str(voltage)
		self._core.io.write(f'SOURce:VOLTage:AUX:LEVel:LIMit:HIGH {param}')

	def get(self) -> float:
		"""SCPI: SOURce:VOLTage:AUX:LEVel:LIMit:HIGH \n
		Snippet: value: float = driver.source.voltage.auxiliary.level.limit.high.get() \n
		This command defines the maximum voltage that may be supplied by the Vaux source. \n
			:return: voltage: numeric value Range: -10 to 10, Unit: V"""
		response = self._core.io.query_str(f'SOURce:VOLTage:AUX:LEVel:LIMit:HIGH?')
		return Conversions.str_to_float(response)
