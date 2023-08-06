from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stop:
	"""Stop commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stop", core, parent)

	def set(self, frequency: float) -> None:
		"""SCPI: [SENSe]:FREQuency:STOP \n
		Snippet: driver.sense.frequency.stop.set(frequency = 1.0) \n
		CW, pulsed and VCO measurements: This command defines the stop frequency offset of the measurement range.
		Transient measurement: This command defines the stop frequency of the transient measurement. Frequency stability
		measurement: The stop frequency offset is coupled to the start time of the frequency stability measurement
		([SENSe:]TIME:STARt) . If you change the stop frequency offset, the start time is adjusted accordingly. For example, 1
		MHz corresponds to 1 ms. \n
			:param frequency: Offset frequencies in half decade steps. Range: See data sheet , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SENSe:FREQuency:STOP {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:FREQuency:STOP \n
		Snippet: value: float = driver.sense.frequency.stop.get() \n
		CW, pulsed and VCO measurements: This command defines the stop frequency offset of the measurement range.
		Transient measurement: This command defines the stop frequency of the transient measurement. Frequency stability
		measurement: The stop frequency offset is coupled to the start time of the frequency stability measurement
		([SENSe:]TIME:STARt) . If you change the stop frequency offset, the start time is adjusted accordingly. For example, 1
		MHz corresponds to 1 ms. \n
			:return: frequency: Offset frequencies in half decade steps. Range: See data sheet , Unit: Hz"""
		response = self._core.io.query_str(f'SENSe:FREQuency:STOP?')
		return Conversions.str_to_float(response)
