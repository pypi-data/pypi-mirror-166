from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: SOURce:GENerator[:STATe] \n
		Snippet: driver.source.generator.state.set(state = False) \n
		This command turns the optional signal source output on and off. When you turn on the signal source, the R&S FSWP
		generates a signal with the frequency and level defined with method RsFswp.Source.Generator.Frequency.set and method
		RsFswp.Source.Generator.Level.set. \n
			:param state: ON | OFF | 1 | 0
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:GENerator:STATe {param}')

	def get(self) -> bool:
		"""SCPI: SOURce:GENerator[:STATe] \n
		Snippet: value: bool = driver.source.generator.state.get() \n
		This command turns the optional signal source output on and off. When you turn on the signal source, the R&S FSWP
		generates a signal with the frequency and level defined with method RsFswp.Source.Generator.Frequency.set and method
		RsFswp.Source.Generator.Level.set. \n
			:return: state: ON | OFF | 1 | 0"""
		response = self._core.io.query_str(f'SOURce:GENerator:STATe?')
		return Conversions.str_to_bool(response)
