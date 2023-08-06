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

	def set(self, state: bool, window=repcap.Window.Default, trace=repcap.Trace.Default) -> None:
		"""SCPI: DISPlay[:WINDow<n>]:TRACe<t>:SMOothing[:STATe] \n
		Snippet: driver.display.window.trace.smoothing.state.set(state = False, window = repcap.Window.Default, trace = repcap.Trace.Default) \n
		This command turns trace smoothing for a specific trace on and off. When you turn on trace smoothing, you can define the
		smoothing magnitude with method RsFswp.Display.Window.Trace.Smoothing.Aperture.set. In the Spot Noise vs Tune measurement,
		trace smoothing applies to either all traces or none. Use [SENSe:]SMOothing[:STATe] in that case. \n
			:param state: ON | OFF | 1 | 0
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:param trace: optional repeated capability selector. Default value: Tr1 (settable in the interface 'Trace')
		"""
		param = Conversions.bool_to_str(state)
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		self._core.io.write(f'DISPlay:WINDow{window_cmd_val}:TRACe{trace_cmd_val}:SMOothing:STATe {param}')

	def get(self, window=repcap.Window.Default, trace=repcap.Trace.Default) -> bool:
		"""SCPI: DISPlay[:WINDow<n>]:TRACe<t>:SMOothing[:STATe] \n
		Snippet: value: bool = driver.display.window.trace.smoothing.state.get(window = repcap.Window.Default, trace = repcap.Trace.Default) \n
		This command turns trace smoothing for a specific trace on and off. When you turn on trace smoothing, you can define the
		smoothing magnitude with method RsFswp.Display.Window.Trace.Smoothing.Aperture.set. In the Spot Noise vs Tune measurement,
		trace smoothing applies to either all traces or none. Use [SENSe:]SMOothing[:STATe] in that case. \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:param trace: optional repeated capability selector. Default value: Tr1 (settable in the interface 'Trace')
			:return: state: ON | OFF | 1 | 0"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		response = self._core.io.query_str(f'DISPlay:WINDow{window_cmd_val}:TRACe{trace_cmd_val}:SMOothing:STATe?')
		return Conversions.str_to_bool(response)
