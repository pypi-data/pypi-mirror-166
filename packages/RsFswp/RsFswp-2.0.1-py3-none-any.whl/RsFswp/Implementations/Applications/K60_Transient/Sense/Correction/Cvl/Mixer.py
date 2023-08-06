from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mixer:
	"""Mixer commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mixer", core, parent)

	def set(self, type_py: str) -> None:
		"""SCPI: [SENSe]:CORRection:CVL:MIXer \n
		Snippet: driver.applications.k60Transient.sense.correction.cvl.mixer.set(type_py = '1') \n
		No command help available \n
			:param type_py: No help available
		"""
		param = Conversions.value_to_quoted_str(type_py)
		self._core.io.write(f'SENSe:CORRection:CVL:MIXer {param}')

	def get(self, type_py: str) -> str:
		"""SCPI: [SENSe]:CORRection:CVL:MIXer \n
		Snippet: value: str = driver.applications.k60Transient.sense.correction.cvl.mixer.get(type_py = '1') \n
		No command help available \n
			:param type_py: No help available
			:return: type_py: No help available"""
		param = Conversions.value_to_quoted_str(type_py)
		response = self._core.io.query_str(f'SENSe:CORRection:CVL:MIXer? {param}')
		return trim_str_response(response)
