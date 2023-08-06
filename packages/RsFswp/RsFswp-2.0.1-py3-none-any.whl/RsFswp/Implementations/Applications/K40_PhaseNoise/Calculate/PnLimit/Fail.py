from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fail:
	"""Fail commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fail", core, parent)

	def get(self, window=repcap.Window.Default) -> bool:
		"""SCPI: CALCulate<n>:PNLimit:FAIL \n
		Snippet: value: bool = driver.applications.k40PhaseNoise.calculate.pnLimit.fail.get(window = repcap.Window.Default) \n
		No command help available \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Calculate')
			:return: limit_check: No help available"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		response = self._core.io.query_str(f'CALCulate{window_cmd_val}:PNLimit:FAIL?')
		return Conversions.str_to_bool(response)
