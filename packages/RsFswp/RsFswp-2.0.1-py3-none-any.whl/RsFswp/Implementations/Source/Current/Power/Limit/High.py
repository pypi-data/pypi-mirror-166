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

	def set(self, current: float, source=repcap.Source.Default) -> None:
		"""SCPI: SOURce:CURRent:POWer<1|2>:LIMit:HIGH \n
		Snippet: driver.source.current.power.limit.high.set(current = 1.0, source = repcap.Source.Default) \n
		This command defines the maximum current of the Vsupply connector.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Vsupply is controlled in terms of voltage (method RsFswp.Applications.K30_NoiseFigure.Source.Voltage.Power.Level.Mode.set) . \n
			:param current: numeric value Range: 0 to 2, Unit: A
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(current)
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		self._core.io.write(f'SOURce:CURRent:POWer{source_cmd_val}:LIMit:HIGH {param}')

	def get(self, source=repcap.Source.Default) -> float:
		"""SCPI: SOURce:CURRent:POWer<1|2>:LIMit:HIGH \n
		Snippet: value: float = driver.source.current.power.limit.high.get(source = repcap.Source.Default) \n
		This command defines the maximum current of the Vsupply connector.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Vsupply is controlled in terms of voltage (method RsFswp.Applications.K30_NoiseFigure.Source.Voltage.Power.Level.Mode.set) . \n
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: current: numeric value Range: 0 to 2, Unit: A"""
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		response = self._core.io.query_str(f'SOURce:CURRent:POWer{source_cmd_val}:LIMit:HIGH?')
		return Conversions.str_to_float(response)
