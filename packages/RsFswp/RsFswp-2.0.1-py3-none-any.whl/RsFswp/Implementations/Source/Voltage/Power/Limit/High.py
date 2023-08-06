from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class High:
	"""High commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("high", core, parent)

	def set(self, voltage: float, source=repcap.Source.Default) -> None:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LIMit:HIGH \n
		Snippet: driver.source.voltage.power.limit.high.set(voltage = 1.0, source = repcap.Source.Default) \n
		This command defines the maximum current or voltage that may be supplied by the Vsupply source. \n
			:param voltage: numeric value The type of value depends on whether you control the output in terms of current or voltage (method RsFswp.Source.Voltage.Power.Level.Mode.set) . When you control it in terms of voltage, the value is a current (A) . When you control it in terms of current, the value is a voltage (V) . Range: 0 to 16 V or 2000 mA, Unit: V or A
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(voltage)
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		self._core.io.write(f'SOURce:VOLTage:POWer{source_cmd_val}:LIMit:HIGH {param}')

	def get(self, source=repcap.Source.Default) -> float:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LIMit:HIGH \n
		Snippet: value: float = driver.source.voltage.power.limit.high.get(source = repcap.Source.Default) \n
		This command defines the maximum current or voltage that may be supplied by the Vsupply source. \n
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: voltage: numeric value The type of value depends on whether you control the output in terms of current or voltage (method RsFswp.Source.Voltage.Power.Level.Mode.set) . When you control it in terms of voltage, the value is a current (A) . When you control it in terms of current, the value is a voltage (V) . Range: 0 to 16 V or 2000 mA, Unit: V or A"""
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		response = self._core.io.query_str(f'SOURce:VOLTage:POWer{source_cmd_val}:LIMit:HIGH?')
		return Conversions.str_to_float(response)
