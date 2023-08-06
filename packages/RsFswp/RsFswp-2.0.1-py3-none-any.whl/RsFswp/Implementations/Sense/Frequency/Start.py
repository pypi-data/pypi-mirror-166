from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Start:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def set(self, frequency: float) -> None:
		"""SCPI: [SENSe]:FREQuency:STARt \n
		Snippet: driver.sense.frequency.start.set(frequency = 1.0) \n
		CW, pulsed and VCO measurements: This command defines the start frequency offset of the measurement range. Transient
		measurement: This command defines the start frequency of the transient measurement. Frequency stability measurement: The
		start frequency offset is coupled to the stop time of the frequency stability measurement ([SENSe:]TIME:STOP) . If you
		change the start frequency offset, the stop time is adjusted accordingly. For example, 1 mHz corresponds to 1000 s. \n
			:param frequency: Offset frequencies in half decade steps. Range: See data sheet , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SENSe:FREQuency:STARt {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:FREQuency:STARt \n
		Snippet: value: float = driver.sense.frequency.start.get() \n
		CW, pulsed and VCO measurements: This command defines the start frequency offset of the measurement range. Transient
		measurement: This command defines the start frequency of the transient measurement. Frequency stability measurement: The
		start frequency offset is coupled to the stop time of the frequency stability measurement ([SENSe:]TIME:STOP) . If you
		change the start frequency offset, the stop time is adjusted accordingly. For example, 1 mHz corresponds to 1000 s. \n
			:return: frequency: Offset frequencies in half decade steps. Range: See data sheet , Unit: Hz"""
		response = self._core.io.query_str(f'SENSe:FREQuency:STARt?')
		return Conversions.str_to_float(response)
