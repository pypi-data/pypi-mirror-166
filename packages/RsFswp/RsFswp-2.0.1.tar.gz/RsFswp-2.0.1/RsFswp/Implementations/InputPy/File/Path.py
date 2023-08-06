from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Path:
	"""Path commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("path", core, parent)

	def set(self, arg_0: str) -> None:
		"""SCPI: INPut:FILE:PATH \n
		Snippet: driver.inputPy.file.path.set(arg_0 = '1') \n
		This command selects the I/Q data file to be used as input for further measurements. The I/Q data must have a specific
		format as described in 'I/Q Data File Format (iq-tar) '. For details see 'Basics on Input from I/Q Data Files'. \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_quoted_str(arg_0)
		self._core.io.write(f'INPut:FILE:PATH {param}')

	def get(self) -> str:
		"""SCPI: INPut:FILE:PATH \n
		Snippet: value: str = driver.inputPy.file.path.get() \n
		This command selects the I/Q data file to be used as input for further measurements. The I/Q data must have a specific
		format as described in 'I/Q Data File Format (iq-tar) '. For details see 'Basics on Input from I/Q Data Files'. \n
			:return: arg_0: No help available"""
		response = self._core.io.query_str(f'INPut:FILE:PATH?')
		return trim_str_response(response)
