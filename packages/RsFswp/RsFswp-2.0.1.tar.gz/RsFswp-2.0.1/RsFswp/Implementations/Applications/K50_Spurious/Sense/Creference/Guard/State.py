from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: [SENSe]:CREFerence:GUARd:STATe \n
		Snippet: driver.applications.k50Spurious.sense.creference.guard.state.set(state = False) \n
		Determines whether the specified guard interval is included in the spur search or not. If the guard interval is not
		included, the spectrum displays contain gaps at the guard intervals. \n
			:param state: ON | OFF | 0 | 1 OFF | 0 Guard interval is not included ON | 1 Guard interval is included
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:CREFerence:GUARd:STATe {param}')

	def get(self) -> bool:
		"""SCPI: [SENSe]:CREFerence:GUARd:STATe \n
		Snippet: value: bool = driver.applications.k50Spurious.sense.creference.guard.state.get() \n
		Determines whether the specified guard interval is included in the spur search or not. If the guard interval is not
		included, the spectrum displays contain gaps at the guard intervals. \n
			:return: state: ON | OFF | 0 | 1 OFF | 0 Guard interval is not included ON | 1 Guard interval is included"""
		response = self._core.io.query_str(f'SENSe:CREFerence:GUARd:STATe?')
		return Conversions.str_to_bool(response)
