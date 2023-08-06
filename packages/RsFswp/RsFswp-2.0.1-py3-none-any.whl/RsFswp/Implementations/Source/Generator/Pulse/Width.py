from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Width:
	"""Width commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("width", core, parent)

	def set(self, pulse_width: float) -> None:
		"""SCPI: SOURce:GENerator:PULSe:WIDTh \n
		Snippet: driver.source.generator.pulse.width.set(pulse_width = 1.0) \n
		This command defines the length of the pulse that is generated.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurements.
			- Turn on signal source (method RsFswp.Source.Generator.State.set) .
			- Turn on pulse modulation (method RsFswp.Source.Generator.Modulation.set) . \n
			:param pulse_width: numeric value Unit: s
		"""
		param = Conversions.decimal_value_to_str(pulse_width)
		self._core.io.write(f'SOURce:GENerator:PULSe:WIDTh {param}')

	def get(self) -> float:
		"""SCPI: SOURce:GENerator:PULSe:WIDTh \n
		Snippet: value: float = driver.source.generator.pulse.width.get() \n
		This command defines the length of the pulse that is generated.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurements.
			- Turn on signal source (method RsFswp.Source.Generator.State.set) .
			- Turn on pulse modulation (method RsFswp.Source.Generator.Modulation.set) . \n
			:return: pulse_width: numeric value Unit: s"""
		response = self._core.io.query_str(f'SOURce:GENerator:PULSe:WIDTh?')
		return Conversions.str_to_float(response)
