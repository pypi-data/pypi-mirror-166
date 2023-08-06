from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coupling:
	"""Coupling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coupling", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: SOURce:VOLTage:CHANnel:COUPling \n
		Snippet: driver.source.voltage.channel.coupling.set(state = False) \n
		This command couples or decouples the DC power configuration across measurement channels. \n
			:param state: ON | 1 DC power configuration is the same across all measurement channels. OFF | 0 DC power configuration is different for each measurement channel.
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:VOLTage:CHANnel:COUPling {param}')

	def get(self) -> bool:
		"""SCPI: SOURce:VOLTage:CHANnel:COUPling \n
		Snippet: value: bool = driver.source.voltage.channel.coupling.get() \n
		This command couples or decouples the DC power configuration across measurement channels. \n
			:return: state: ON | 1 DC power configuration is the same across all measurement channels. OFF | 0 DC power configuration is different for each measurement channel."""
		response = self._core.io.query_str(f'SOURce:VOLTage:CHANnel:COUPling?')
		return Conversions.str_to_bool(response)
