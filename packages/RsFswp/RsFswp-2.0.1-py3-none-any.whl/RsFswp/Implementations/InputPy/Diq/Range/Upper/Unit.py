from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unit:
	"""Unit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("unit", core, parent)

	def set(self, arg_0: enums.DiqUnit) -> None:
		"""SCPI: INPut:DIQ:RANGe[:UPPer]:UNIT \n
		Snippet: driver.inputPy.diq.range.upper.unit.set(arg_0 = enums.DiqUnit.AMPere) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.enum_scalar_to_str(arg_0, enums.DiqUnit)
		self._core.io.write(f'INPut:DIQ:RANGe:UPPer:UNIT {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.DiqUnit:
		"""SCPI: INPut:DIQ:RANGe[:UPPer]:UNIT \n
		Snippet: value: enums.DiqUnit = driver.inputPy.diq.range.upper.unit.get() \n
		No command help available \n
			:return: arg_0: No help available"""
		response = self._core.io.query_str(f'INPut:DIQ:RANGe:UPPer:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.DiqUnit)
