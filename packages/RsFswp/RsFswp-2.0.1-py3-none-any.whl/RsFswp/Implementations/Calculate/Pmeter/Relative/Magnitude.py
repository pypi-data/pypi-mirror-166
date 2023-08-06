from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Magnitude:
	"""Magnitude commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("magnitude", core, parent)

	def set(self, ref_value: float, window=repcap.Window.Default, powerMeter=repcap.PowerMeter.Default) -> None:
		"""SCPI: CALCulate<n>:PMETer<p>:RELative[:MAGNitude] \n
		Snippet: driver.calculate.pmeter.relative.magnitude.set(ref_value = 1.0, window = repcap.Window.Default, powerMeter = repcap.PowerMeter.Default) \n
		No command help available \n
			:param ref_value: No help available
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param powerMeter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmeter')
		"""
		param = Conversions.decimal_value_to_str(ref_value)
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		powerMeter_cmd_val = self._cmd_group.get_repcap_cmd_value(powerMeter, repcap.PowerMeter)
		self._core.io.write(f'CALCulate{window_cmd_val}:PMETer{powerMeter_cmd_val}:RELative:MAGNitude {param}')

	def get(self, window=repcap.Window.Default, powerMeter=repcap.PowerMeter.Default) -> float:
		"""SCPI: CALCulate<n>:PMETer<p>:RELative[:MAGNitude] \n
		Snippet: value: float = driver.calculate.pmeter.relative.magnitude.get(window = repcap.Window.Default, powerMeter = repcap.PowerMeter.Default) \n
		No command help available \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:param powerMeter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmeter')
			:return: ref_value: No help available"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		powerMeter_cmd_val = self._cmd_group.get_repcap_cmd_value(powerMeter, repcap.PowerMeter)
		response = self._core.io.query_str(f'CALCulate{window_cmd_val}:PMETer{powerMeter_cmd_val}:RELative:MAGNitude?')
		return Conversions.str_to_float(response)
