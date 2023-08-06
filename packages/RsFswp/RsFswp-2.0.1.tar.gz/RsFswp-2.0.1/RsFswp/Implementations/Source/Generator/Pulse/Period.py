from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Period:
	"""Period commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("period", core, parent)

	def set(self, pulse_period: float) -> None:
		"""SCPI: SOURce:GENerator:PULSe:PERiod \n
		Snippet: driver.source.generator.pulse.period.set(pulse_period = 1.0) \n
		This command defines the pulse period (distance between two consecutive pulses) of the pulse that is generated.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurements.
			- Turn on signal source (method RsFswp.Source.Generator.State.set) .
			- Turn on pulse modulation (method RsFswp.Source.Generator.Modulation.set) . \n
			:param pulse_period: numeric value Unit: s
		"""
		param = Conversions.decimal_value_to_str(pulse_period)
		self._core.io.write(f'SOURce:GENerator:PULSe:PERiod {param}')

	def get(self) -> float:
		"""SCPI: SOURce:GENerator:PULSe:PERiod \n
		Snippet: value: float = driver.source.generator.pulse.period.get() \n
		This command defines the pulse period (distance between two consecutive pulses) of the pulse that is generated.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurements.
			- Turn on signal source (method RsFswp.Source.Generator.State.set) .
			- Turn on pulse modulation (method RsFswp.Source.Generator.Modulation.set) . \n
			:return: pulse_period: numeric value Unit: s"""
		response = self._core.io.query_str(f'SOURce:GENerator:PULSe:PERiod?')
		return Conversions.str_to_float(response)
