from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	def set(self, pulse_output: enums.SignalLevel) -> None:
		"""SCPI: SOURce:GENerator:PULSe:TRIGger:OUTPut \n
		Snippet: driver.source.generator.pulse.trigger.output.set(pulse_output = enums.SignalLevel.HIGH) \n
		This command selects the signal type provided at the trigger output connector. The signal can be used, for example, to
		control an external pulse modulator. \n
			:param pulse_output: HIGH Provides a high active pulse at the trigger output. Note that the signal is provided even if internal pulse modulation has been turned off. You can define the pulse characteristics with •method RsFswp.Source.Generator.Pulse.Width.set •method RsFswp.Source.Generator.Pulse.Period.set LOW Provides a low active pulse at the trigger output. Note that the signal is provided even if internal pulse modulation has been turned off. OFF | 0 Provides no signal at the trigger output.
		"""
		param = Conversions.enum_scalar_to_str(pulse_output, enums.SignalLevel)
		self._core.io.write(f'SOURce:GENerator:PULSe:TRIGger:OUTPut {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.SignalLevel:
		"""SCPI: SOURce:GENerator:PULSe:TRIGger:OUTPut \n
		Snippet: value: enums.SignalLevel = driver.source.generator.pulse.trigger.output.get() \n
		This command selects the signal type provided at the trigger output connector. The signal can be used, for example, to
		control an external pulse modulator. \n
			:return: pulse_output: No help available"""
		response = self._core.io.query_str(f'SOURce:GENerator:PULSe:TRIGger:OUTPut?')
		return Conversions.str_to_scalar_enum(response, enums.SignalLevel)
