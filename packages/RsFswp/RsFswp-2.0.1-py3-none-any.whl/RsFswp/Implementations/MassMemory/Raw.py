from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Raw:
	"""Raw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("raw", core, parent)

	def set(self, path: str) -> None:
		"""SCPI: MMEMory:RAW \n
		Snippet: driver.massMemory.raw.set(path = '1') \n
		No command help available \n
			:param path: No help available
		"""
		param = Conversions.value_to_quoted_str(path)
		self._core.io.write(f'MMEMory:RAW {param}')

	def get(self) -> str:
		"""SCPI: MMEMory:RAW \n
		Snippet: value: str = driver.massMemory.raw.get() \n
		No command help available \n
			:return: path: No help available"""
		response = self._core.io.query_str(f'MMEMory:RAW?')
		return trim_str_response(response)
