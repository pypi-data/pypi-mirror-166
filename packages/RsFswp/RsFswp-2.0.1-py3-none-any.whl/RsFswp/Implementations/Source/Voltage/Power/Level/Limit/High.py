from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class High:
	"""High commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("high", core, parent)

	def set(self, voltage_current: float, source=repcap.Source.Default) -> None:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LEVel:LIMit:HIGH \n
		Snippet: driver.source.voltage.power.level.limit.high.set(voltage_current = 1.0, source = repcap.Source.Default) \n
		This command defines the maximum voltage that may be supplied by the Vsupply source. \n
			:param voltage_current: No help available
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(voltage_current)
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		self._core.io.write(f'SOURce:VOLTage:POWer{source_cmd_val}:LEVel:LIMit:HIGH {param}')

	def get(self, source=repcap.Source.Default) -> float:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LEVel:LIMit:HIGH \n
		Snippet: value: float = driver.source.voltage.power.level.limit.high.get(source = repcap.Source.Default) \n
		This command defines the maximum voltage that may be supplied by the Vsupply source. \n
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: voltage_current: No help available"""
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		response = self._core.io.query_str(f'SOURce:VOLTage:POWer{source_cmd_val}:LEVel:LIMit:HIGH?')
		return Conversions.str_to_float(response)
