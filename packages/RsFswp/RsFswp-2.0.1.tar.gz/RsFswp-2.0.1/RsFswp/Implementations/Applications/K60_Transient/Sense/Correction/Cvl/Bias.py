from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bias:
	"""Bias commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bias", core, parent)

	def set(self, bias_setting: float) -> None:
		"""SCPI: [SENSe]:CORRection:CVL:BIAS \n
		Snippet: driver.applications.k60Transient.sense.correction.cvl.bias.set(bias_setting = 1.0) \n
		No command help available \n
			:param bias_setting: No help available
		"""
		param = Conversions.decimal_value_to_str(bias_setting)
		self._core.io.write(f'SENSe:CORRection:CVL:BIAS {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:CORRection:CVL:BIAS \n
		Snippet: value: float = driver.applications.k60Transient.sense.correction.cvl.bias.get() \n
		No command help available \n
			:return: bias_setting: No help available"""
		response = self._core.io.query_str(f'SENSe:CORRection:CVL:BIAS?')
		return Conversions.str_to_float(response)
