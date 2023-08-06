from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Link:
	"""Link commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("link", core, parent)

	def set(self, type_py: enums.GeneratorLink, generator=repcap.Generator.Default) -> None:
		"""SCPI: SYSTem:COMMunicate:RDEVice:GENerator<gen>:LINK \n
		Snippet: driver.system.communicate.rdevice.generator.link.set(type_py = enums.GeneratorLink.GPIB, generator = repcap.Generator.Default) \n
		No command help available \n
			:param type_py: No help available
			:param generator: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Generator')
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.GeneratorLink)
		generator_cmd_val = self._cmd_group.get_repcap_cmd_value(generator, repcap.Generator)
		self._core.io.write(f'SYSTem:COMMunicate:RDEVice:GENerator{generator_cmd_val}:LINK {param}')

	# noinspection PyTypeChecker
	def get(self, generator=repcap.Generator.Default) -> enums.GeneratorLink:
		"""SCPI: SYSTem:COMMunicate:RDEVice:GENerator<gen>:LINK \n
		Snippet: value: enums.GeneratorLink = driver.system.communicate.rdevice.generator.link.get(generator = repcap.Generator.Default) \n
		No command help available \n
			:param generator: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Generator')
			:return: type_py: No help available"""
		generator_cmd_val = self._cmd_group.get_repcap_cmd_value(generator, repcap.Generator)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:RDEVice:GENerator{generator_cmd_val}:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorLink)
