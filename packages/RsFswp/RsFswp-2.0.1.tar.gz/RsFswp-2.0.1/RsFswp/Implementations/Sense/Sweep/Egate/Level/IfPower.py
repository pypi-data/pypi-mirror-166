from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IfPower:
	"""IfPower commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ifPower", core, parent)

	def set(self, gate_level: float) -> None:
		"""SCPI: [SENSe]:SWEep:EGATe:LEVel:IFPower \n
		Snippet: driver.sense.sweep.egate.level.ifPower.set(gate_level = 1.0) \n
		No command help available \n
			:param gate_level: No help available
		"""
		param = Conversions.decimal_value_to_str(gate_level)
		self._core.io.write(f'SENSe:SWEep:EGATe:LEVel:IFPower {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:SWEep:EGATe:LEVel:IFPower \n
		Snippet: value: float = driver.sense.sweep.egate.level.ifPower.get() \n
		No command help available \n
			:return: gate_level: No help available"""
		response = self._core.io.query_str(f'SENSe:SWEep:EGATe:LEVel:IFPower?')
		return Conversions.str_to_float(response)
