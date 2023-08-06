from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.LoadType) -> None:
		"""SCPI: MMEMory:LOAD:TYPE \n
		Snippet: driver.massMemory.load.typePy.set(type_py = enums.LoadType.NEW) \n
		No command help available \n
			:param type_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.LoadType)
		self._core.io.write(f'MMEMory:LOAD:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.LoadType:
		"""SCPI: MMEMory:LOAD:TYPE \n
		Snippet: value: enums.LoadType = driver.massMemory.load.typePy.get() \n
		No command help available \n
			:return: type_py: No help available"""
		response = self._core.io.query_str(f'MMEMory:LOAD:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.LoadType)
