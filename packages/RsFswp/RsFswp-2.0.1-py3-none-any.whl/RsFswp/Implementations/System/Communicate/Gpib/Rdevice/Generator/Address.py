from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Address:
	"""Address commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("address", core, parent)

	def set(self, number: int, generator=repcap.Generator.Default) -> None:
		"""SCPI: SYSTem:COMMunicate:GPIB:RDEVice:GENerator<gen>:ADDRess \n
		Snippet: driver.system.communicate.gpib.rdevice.generator.address.set(number = 1, generator = repcap.Generator.Default) \n
		No command help available \n
			:param number: No help available
			:param generator: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Generator')
		"""
		param = Conversions.decimal_value_to_str(number)
		generator_cmd_val = self._cmd_group.get_repcap_cmd_value(generator, repcap.Generator)
		self._core.io.write(f'SYSTem:COMMunicate:GPIB:RDEVice:GENerator{generator_cmd_val}:ADDRess {param}')

	def get(self, generator=repcap.Generator.Default) -> int:
		"""SCPI: SYSTem:COMMunicate:GPIB:RDEVice:GENerator<gen>:ADDRess \n
		Snippet: value: int = driver.system.communicate.gpib.rdevice.generator.address.get(generator = repcap.Generator.Default) \n
		No command help available \n
			:param generator: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Generator')
			:return: number: No help available"""
		generator_cmd_val = self._cmd_group.get_repcap_cmd_value(generator, repcap.Generator)
		response = self._core.io.query_str(f'SYSTem:COMMunicate:GPIB:RDEVice:GENerator{generator_cmd_val}:ADDRess?')
		return Conversions.str_to_int(response)
