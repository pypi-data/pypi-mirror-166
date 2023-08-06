from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generate:
	"""Generate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("generate", core, parent)

	def set(self, name: str) -> None:
		"""SCPI: [SENSe]:CORRection:TRANsducer:GENerate \n
		Snippet: driver.sense.correction.transducer.generate.set(name = '1') \n
		No command help available \n
			:param name: No help available
		"""
		param = Conversions.value_to_quoted_str(name)
		self._core.io.write(f'SENSe:CORRection:TRANsducer:GENerate {param}')

	def get(self) -> str:
		"""SCPI: [SENSe]:CORRection:TRANsducer:GENerate \n
		Snippet: value: str = driver.sense.correction.transducer.generate.get() \n
		No command help available \n
			:return: name: No help available"""
		response = self._core.io.query_str(f'SENSe:CORRection:TRANsducer:GENerate?')
		return trim_str_response(response)
