from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sstart:
	"""Sstart commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sstart", core, parent)

	def get(self, window=repcap.Window.Default) -> List[float]:
		"""SCPI: TRACe<n>:IQ:SCAPture:TSTamp:SSTart \n
		Snippet: value: List[float] = driver.trace.iq.scapture.tstamp.sstart.get(window = repcap.Window.Default) \n
		No command help available \n
			:param window: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trace')
			:return: timestamps: No help available"""
		window_cmd_val = self._cmd_group.get_repcap_cmd_value(window, repcap.Window)
		response = self._core.io.query_bin_or_ascii_float_list(f'TRACe{window_cmd_val}:IQ:SCAPture:TSTamp:SSTart?')
		return response
