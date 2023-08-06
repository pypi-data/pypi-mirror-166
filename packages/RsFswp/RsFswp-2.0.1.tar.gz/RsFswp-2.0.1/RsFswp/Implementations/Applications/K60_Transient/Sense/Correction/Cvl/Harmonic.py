from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Harmonic:
	"""Harmonic commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("harmonic", core, parent)

	def set(self, harm_order: float) -> None:
		"""SCPI: [SENSe]:CORRection:CVL:HARMonic \n
		Snippet: driver.applications.k60Transient.sense.correction.cvl.harmonic.set(harm_order = 1.0) \n
		No command help available \n
			:param harm_order: No help available
		"""
		param = Conversions.decimal_value_to_str(harm_order)
		self._core.io.write(f'SENSe:CORRection:CVL:HARMonic {param}')

	def get(self, harm_order: float) -> float:
		"""SCPI: [SENSe]:CORRection:CVL:HARMonic \n
		Snippet: value: float = driver.applications.k60Transient.sense.correction.cvl.harmonic.get(harm_order = 1.0) \n
		No command help available \n
			:param harm_order: No help available
			:return: harm_order: No help available"""
		param = Conversions.decimal_value_to_str(harm_order)
		response = self._core.io.query_str(f'SENSe:CORRection:CVL:HARMonic? {param}')
		return Conversions.str_to_float(response)
