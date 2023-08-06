from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Date:
	"""Date commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("date", core, parent)

	def get(self) -> str:
		"""SCPI: SYSTem:COMMunicate:RDEVice:OSCilloscope:ALIGnment:DATE \n
		Snippet: value: str = driver.system.communicate.rdevice.oscilloscope.alignment.date.get() \n
		No command help available \n
			:return: alignment_date: No help available"""
		response = self._core.io.query_str(f'SYSTem:COMMunicate:RDEVice:OSCilloscope:ALIGnment:DATE?')
		return trim_str_response(response)
