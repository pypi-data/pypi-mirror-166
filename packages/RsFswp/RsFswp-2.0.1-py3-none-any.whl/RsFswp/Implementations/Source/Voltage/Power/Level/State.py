from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, source=repcap.Source.Default) -> None:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LEVel[:STATe] \n
		Snippet: driver.source.voltage.power.level.state.set(state = False, source = repcap.Source.Default) \n
		This command turns the supply voltage source (Vsupply) on and off. Note that DC power is actually supplied only if you
		additionally activate the outputs in general.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on DC power sources (method RsFswp.Source.Voltage.State.set) . \n
			:param state: ON | OFF | 1 | 0
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.bool_to_str(state)
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		self._core.io.write(f'SOURce:VOLTage:POWer{source_cmd_val}:LEVel:STATe {param}')

	def get(self, source=repcap.Source.Default) -> bool:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LEVel[:STATe] \n
		Snippet: value: bool = driver.source.voltage.power.level.state.get(source = repcap.Source.Default) \n
		This command turns the supply voltage source (Vsupply) on and off. Note that DC power is actually supplied only if you
		additionally activate the outputs in general.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on DC power sources (method RsFswp.Source.Voltage.State.set) . \n
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: state: ON | OFF | 1 | 0"""
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		response = self._core.io.query_str(f'SOURce:VOLTage:POWer{source_cmd_val}:LEVel:STATe?')
		return Conversions.str_to_bool(response)
