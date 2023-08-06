from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, name: str, generator=repcap.Generator.Default) -> None:
		"""SCPI: SYSTem:COMMunicate:RDEVice:GENerator<gen>:TYPE \n
		Snippet: driver.system.communicate.rdevice.generator.typePy.set(name = '1', generator = repcap.Generator.Default) \n
		No command help available \n
			:param name: No help available
			:param generator: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Generator')
		"""
		param = Conversions.value_to_quoted_str(name)
		generator_cmd_val = self._cmd_group.get_repcap_cmd_value(generator, repcap.Generator)
		self._core.io.write(f'SYSTem:COMMunicate:RDEVice:GENerator{generator_cmd_val}:TYPE {param}')

	def get(self, generator=repcap.Generator.Default) -> str:
		"""SCPI: SYSTem:COMMunicate:RDEVice:GENerator<gen>:TYPE \n
		Snippet: value: str = driver.system.communicate.rdevice.generator.typePy.get(generator = repcap.Generator.Default) \n
		No command help available \n
			:param generator: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Generator')
			:return: name: No help available"""
		generator_cmd_val = self._cmd_group.get_repcap_cmd_value(generator, repcap.Generator)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:RDEVice:GENerator{generator_cmd_val}:TYPE?')
		return trim_str_response(response)
