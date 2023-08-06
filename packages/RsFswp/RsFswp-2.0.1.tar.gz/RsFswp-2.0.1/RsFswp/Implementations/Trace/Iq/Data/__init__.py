from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	@property
	def memory(self):
		"""memory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_memory'):
			from .Memory import Memory
			self._memory = Memory(self._core, self._cmd_group)
		return self._memory

	def get(self) -> List[float]:
		"""SCPI: TRACe:IQ:DATA \n
		Snippet: value: List[float] = driver.trace.iq.data.get() \n
		This command initiates a measurement with the current settings and returns the captured data from I/Q measurements. This
		command corresponds to: INIT:IMM;*WAI;method RsFswp.Trace.Iq.Data.Memory.get_ However, the method RsFswp.Trace.Iq.Data.
		get_ command is quicker in comparison. Note: Using the command with the *RST values for the TRACe:IQ:SET command, the
		following minimum buffer sizes for the response data are recommended: ASCII format 10 kBytes, binary format: 2 kBytes \n
			:return: iq_data: Measured voltage for I and Q component for each sample that has been captured during the measurement. The number of samples depends on TRACe:IQ:SET. In ASCII format, the number of results is 2* the number of samples. The data format depends on TRACe:IQ:DATA:FORMat. Unit: V"""
		response = self._core.io.query_bin_or_ascii_float_list_with_opc(f'FORMAT REAL,32;TRACe:IQ:DATA?')
		return response

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
