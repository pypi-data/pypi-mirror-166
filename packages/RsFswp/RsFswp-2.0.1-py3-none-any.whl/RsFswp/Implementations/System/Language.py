from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Language:
	"""Language commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("language", core, parent)

	def set(self, language: str) -> None:
		"""SCPI: SYSTem:LANGuage \n
		Snippet: driver.system.language.set(language = '1') \n
		This command selects the system language. \n
			:param language: String containing the name of the language. 'SCPI' SCPI language. 'PSA' PSA emulation. For a list of supported commands, see 'Reference: Command Set of Emulated PSA Models'.
		"""
		param = Conversions.value_to_quoted_str(language)
		self._core.io.write(f'SYSTem:LANGuage {param}')

	def get(self) -> str:
		"""SCPI: SYSTem:LANGuage \n
		Snippet: value: str = driver.system.language.get() \n
		This command selects the system language. \n
			:return: language: String containing the name of the language. 'SCPI' SCPI language. 'PSA' PSA emulation. For a list of supported commands, see 'Reference: Command Set of Emulated PSA Models'."""
		response = self._core.io.query_str(f'SYSTem:LANGuage?')
		return trim_str_response(response)
