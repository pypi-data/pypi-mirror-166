from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def set(self, state: bool, outputConnector=repcap.OutputConnector.Default, probe=repcap.Probe.Default) -> None:
		"""SCPI: OUTPut<up>:PROBe<pb>[:POWer] \n
		Snippet: driver.output.probe.power.set(state = False, outputConnector = repcap.OutputConnector.Default, probe = repcap.Probe.Default) \n
		No command help available \n
			:param state: No help available
			:param outputConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:param probe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Probe')
		"""
		param = Conversions.bool_to_str(state)
		outputConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(outputConnector, repcap.OutputConnector)
		probe_cmd_val = self._cmd_group.get_repcap_cmd_value(probe, repcap.Probe)
		self._core.io.write(f'OUTPut{outputConnector_cmd_val}:PROBe{probe_cmd_val}:POWer {param}')

	def get(self, outputConnector=repcap.OutputConnector.Default, probe=repcap.Probe.Default) -> bool:
		"""SCPI: OUTPut<up>:PROBe<pb>[:POWer] \n
		Snippet: value: bool = driver.output.probe.power.get(outputConnector = repcap.OutputConnector.Default, probe = repcap.Probe.Default) \n
		No command help available \n
			:param outputConnector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:param probe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Probe')
			:return: state: No help available"""
		outputConnector_cmd_val = self._cmd_group.get_repcap_cmd_value(outputConnector, repcap.OutputConnector)
		probe_cmd_val = self._cmd_group.get_repcap_cmd_value(probe, repcap.Probe)
		response = self._core.io.query_str(f'OUTPut{outputConnector_cmd_val}:PROBe{probe_cmd_val}:POWer?')
		return Conversions.str_to_bool(response)
