from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, offset: float, externalGen=repcap.ExternalGen.Nr1) -> None:
		"""SCPI: SOURce:EXTernal<gen>:FREQuency:OFFSet \n
		Snippet: driver.source.external.frequency.offset.set(offset = 1.0, externalGen = repcap.ExternalGen.Nr1) \n
		No command help available \n
			:param offset: No help available
			:param externalGen: optional repeated capability selector. Default value: Nr1
		"""
		param = Conversions.decimal_value_to_str(offset)
		externalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(externalGen, repcap.ExternalGen)
		self._core.io.write(f'SOURce:EXTernal{externalGen_cmd_val}:FREQuency:OFFSet {param}')

	def get(self, externalGen=repcap.ExternalGen.Nr1) -> float:
		"""SCPI: SOURce:EXTernal<gen>:FREQuency:OFFSet \n
		Snippet: value: float = driver.source.external.frequency.offset.get(externalGen = repcap.ExternalGen.Nr1) \n
		No command help available \n
			:param externalGen: optional repeated capability selector. Default value: Nr1
			:return: offset: No help available"""
		externalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(externalGen, repcap.ExternalGen)
		response = self._core.io.query_str(f'SOURce:EXTernal{externalGen_cmd_val}:FREQuency:OFFSet?')
		return Conversions.str_to_float(response)
