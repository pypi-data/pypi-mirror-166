from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, auto_mode: bool) -> None:
		"""SCPI: CALibration:AIQ:HATiming[:STATe] \n
		Snippet: driver.calibration.aiq.haTiming.state.set(auto_mode = False) \n
		No command help available \n
			:param auto_mode: No help available
		"""
		param = Conversions.bool_to_str(auto_mode)
		self._core.io.write(f'CALibration:AIQ:HATiming:STATe {param}')

	def get(self) -> bool:
		"""SCPI: CALibration:AIQ:HATiming[:STATe] \n
		Snippet: value: bool = driver.calibration.aiq.haTiming.state.get() \n
		No command help available \n
			:return: auto_mode: No help available"""
		response = self._core.io.query_str(f'CALibration:AIQ:HATiming:STATe?')
		return Conversions.str_to_bool(response)
