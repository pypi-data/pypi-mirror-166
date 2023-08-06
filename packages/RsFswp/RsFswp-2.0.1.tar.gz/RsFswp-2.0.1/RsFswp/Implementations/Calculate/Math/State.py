from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, window=repcap.Window.Default) -> None:
		"""SCPI: CALCulate<n>:MATH:STATe \n
		Snippet: driver.calculate.math.state.set(state = False, window = repcap.Window.Default) \n
		This command turns trace mathematics on and off. \n
			:param state: ON | 1 Turns trace mathematics on and selects the operation that has been selected last (or (TRACE1-TRACE3) if you have not yet selected one) . OFF | 0 Turns trace mathematics off.
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
		"""
		param = Conversions.bool_to_str(state)
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		self._core.io.write(f'CALCulate{window_cmd_val}:MATH:STATe {param}')

	def get(self, window=repcap.Window.Default) -> bool:
		"""SCPI: CALCulate<n>:MATH:STATe \n
		Snippet: value: bool = driver.calculate.math.state.get(window = repcap.Window.Default) \n
		This command turns trace mathematics on and off. \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:return: state: ON | 1 Turns trace mathematics on and selects the operation that has been selected last (or (TRACE1-TRACE3) if you have not yet selected one) . OFF | 0 Turns trace mathematics off."""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		response = self._core.io.query_str(f'CALCulate{window_cmd_val}:MATH:STATe?')
		return Conversions.str_to_bool(response)
