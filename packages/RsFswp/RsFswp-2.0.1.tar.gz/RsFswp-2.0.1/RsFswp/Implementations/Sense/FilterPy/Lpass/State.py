from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, filterPy=repcap.FilterPy.Default) -> None:
		"""SCPI: [SENSe]:FILTer<n>:LPASs[:STATe] \n
		Snippet: driver.sense.filterPy.lpass.state.set(state = False, filterPy = repcap.FilterPy.Default) \n
		This command turns a low pass filter for measurements on small carrier frequencies on and off.
			INTRO_CMD_HELP: Effects of using thelow pass filter: \n
			- Auto search feature is turned off ([SENSe:]ADJust:CONFigure:FREQuency:AUTosearch[:STATe]) .
			- Signal count is turned off ([SENSe:]ADJust:CONFigure:FREQuency:COUNt) .
			- The stop offset is limited to 30 % of the filter cut-off frequency ([SENSe:]FREQuency:STOP) .
			- DC coupling should be used for measurements on carrier frequencies below 1 MHz (method RsFswp.Applications.K30_NoiseFigure.InputPy.Coupling.set) . \n
			:param state: ON | OFF | 1 | 0 When you turn on the filter, you can define a cutoff frequency with [SENSe:]FILTer:LPASs:FREQuency:MANual.
			:param filterPy: optional repeated capability selector. Default value: Nr1 (settable in the interface 'FilterPy')
		"""
		param = Conversions.bool_to_str(state)
		filterPy_cmd_val = self._cmd_group.get_repcap_cmd_value(filterPy, repcap.FilterPy)
		self._core.io.write(f'SENSe:FILTer{filterPy_cmd_val}:LPASs:STATe {param}')

	def get(self, filterPy=repcap.FilterPy.Default) -> bool:
		"""SCPI: [SENSe]:FILTer<n>:LPASs[:STATe] \n
		Snippet: value: bool = driver.sense.filterPy.lpass.state.get(filterPy = repcap.FilterPy.Default) \n
		This command turns a low pass filter for measurements on small carrier frequencies on and off.
			INTRO_CMD_HELP: Effects of using thelow pass filter: \n
			- Auto search feature is turned off ([SENSe:]ADJust:CONFigure:FREQuency:AUTosearch[:STATe]) .
			- Signal count is turned off ([SENSe:]ADJust:CONFigure:FREQuency:COUNt) .
			- The stop offset is limited to 30 % of the filter cut-off frequency ([SENSe:]FREQuency:STOP) .
			- DC coupling should be used for measurements on carrier frequencies below 1 MHz (method RsFswp.Applications.K30_NoiseFigure.InputPy.Coupling.set) . \n
			:param filterPy: optional repeated capability selector. Default value: Nr1 (settable in the interface 'FilterPy')
			:return: state: ON | OFF | 1 | 0 When you turn on the filter, you can define a cutoff frequency with [SENSe:]FILTer:LPASs:FREQuency:MANual."""
		filterPy_cmd_val = self._cmd_group.get_repcap_cmd_value(filterPy, repcap.FilterPy)
		response = self._core.io.query_str(f'SENSe:FILTer{filterPy_cmd_val}:LPASs:STATe?')
		return Conversions.str_to_bool(response)
