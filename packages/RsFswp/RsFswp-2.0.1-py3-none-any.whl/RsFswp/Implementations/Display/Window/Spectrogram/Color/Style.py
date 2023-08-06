from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Style:
	"""Style commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("style", core, parent)

	def set(self, color_scheme: enums.ColorSchemeA, window=repcap.Window.Default) -> None:
		"""SCPI: DISPlay[:WINDow<n>]:SPECtrogram:COLor[:STYLe] \n
		Snippet: driver.display.window.spectrogram.color.style.set(color_scheme = enums.ColorSchemeA.COLD, window = repcap.Window.Default) \n
		No command help available \n
			:param color_scheme: No help available
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
		"""
		param = Conversions.enum_scalar_to_str(color_scheme, enums.ColorSchemeA)
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		self._core.io.write(f'DISPlay:WINDow{window_cmd_val}:SPECtrogram:COLor:STYLe {param}')

	# noinspection PyTypeChecker
	def get(self, window=repcap.Window.Default) -> enums.ColorSchemeA:
		"""SCPI: DISPlay[:WINDow<n>]:SPECtrogram:COLor[:STYLe] \n
		Snippet: value: enums.ColorSchemeA = driver.display.window.spectrogram.color.style.get(window = repcap.Window.Default) \n
		No command help available \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Window')
			:return: color_scheme: No help available"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		response = self._core.io.query_str(f'DISPlay:WINDow{window_cmd_val}:SPECtrogram:COLor:STYLe?')
		return Conversions.str_to_scalar_enum(response, enums.ColorSchemeA)
