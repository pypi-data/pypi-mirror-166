from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ftype:
	"""Ftype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ftype", core, parent)

	def set(self, filter_type: enums.FilterTypeC) -> None:
		"""SCPI: [SENSe]:MPOWer:FTYPe \n
		Snippet: driver.sense.mpower.ftype.set(filter_type = enums.FilterTypeC.CFILter) \n
		No command help available \n
			:param filter_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(filter_type, enums.FilterTypeC)
		self._core.io.write(f'SENSe:MPOWer:FTYPe {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.FilterTypeC:
		"""SCPI: [SENSe]:MPOWer:FTYPe \n
		Snippet: value: enums.FilterTypeC = driver.sense.mpower.ftype.get() \n
		No command help available \n
			:return: filter_type: No help available"""
		response = self._core.io.query_str(f'SENSe:MPOWer:FTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.FilterTypeC)
