from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulation", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: SOURce:GENerator:MODulation \n
		Snippet: driver.source.generator.modulation.set(state = False) \n
		This command turns internal pulse modulation for pulsed measurements on and off. \n
			:param state: ON | 1 A pulse is output on the signal source. You can define the pulse characteristics with •method RsFswp.Source.Generator.Pulse.Period.set •method RsFswp.Source.Generator.Pulse.Width.set OFF | 0 A sine signal is output on the signal source.
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:GENerator:MODulation {param}')

	def get(self) -> bool:
		"""SCPI: SOURce:GENerator:MODulation \n
		Snippet: value: bool = driver.source.generator.modulation.get() \n
		This command turns internal pulse modulation for pulsed measurements on and off. \n
			:return: state: ON | 1 A pulse is output on the signal source. You can define the pulse characteristics with •method RsFswp.Source.Generator.Pulse.Period.set •method RsFswp.Source.Generator.Pulse.Width.set OFF | 0 A sine signal is output on the signal source."""
		response = self._core.io.query_str(f'SOURce:GENerator:MODulation?')
		return Conversions.str_to_bool(response)
