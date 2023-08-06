from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sequence", core, parent)

	# noinspection PyTypeChecker
	class SequenceStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Frequency: List[float]: No parameter help available
			- Ref_Level: List[float]: No parameter help available
			- Rfattenuation: List[float]: No parameter help available
			- Filter_Type: List[float or bool]: No parameter help available
			- Rbw: List[enums.FilterTypeK91]: No parameter help available
			- Vbw: List[float]: No parameter help available
			- Meas_Time: List[float]: No parameter help available
			- Trigger_Level: List[float]: No parameter help available
			- Power_Level: List[float]: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Frequency', DataType.FloatList, None, False, True, 1),
			ArgStruct('Ref_Level', DataType.FloatList, None, False, True, 1),
			ArgStruct('Rfattenuation', DataType.FloatList, None, False, True, 1),
			ArgStruct('Filter_Type', DataType.FloatList, None, False, True, 1),
			ArgStruct('Rbw', DataType.EnumList, enums.FilterTypeK91, False, True, 1),
			ArgStruct('Vbw', DataType.FloatList, None, False, True, 1),
			ArgStruct('Meas_Time', DataType.FloatList, None, False, True, 1),
			ArgStruct('Trigger_Level', DataType.FloatList, None, False, True, 1),
			ArgStruct('Power_Level', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency: List[float] = None
			self.Ref_Level: List[float] = None
			self.Rfattenuation: List[float] = None
			self.Filter_Type: List[float or bool] = None
			self.Rbw: List[enums.FilterTypeK91] = None
			self.Vbw: List[float] = None
			self.Meas_Time: List[float] = None
			self.Trigger_Level: List[float] = None
			self.Power_Level: List[float] = None

	def set(self, structure: SequenceStruct) -> None:
		"""SCPI: [SENSe]:LIST:POWer[:SEQuence] \n
		Snippet with structure: \n
		structure = driver.sense.listPy.power.sequence.SequenceStruct() \n
		structure.Frequency: List[float] = [1.1, 2.2, 3.3] \n
		structure.Ref_Level: List[float] = [1.1, 2.2, 3.3] \n
		structure.Rfattenuation: List[float] = [1.1, 2.2, 3.3] \n
		structure.Filter_Type: List[float or bool] = [1.1, True, 2.2, False, 3.3] \n
		structure.Rbw: List[enums.FilterTypeK91] = [FilterTypeK91.CFILter, FilterTypeK91.RRC] \n
		structure.Vbw: List[float] = [1.1, 2.2, 3.3] \n
		structure.Meas_Time: List[float] = [1.1, 2.2, 3.3] \n
		structure.Trigger_Level: List[float] = [1.1, 2.2, 3.3] \n
		structure.Power_Level: List[float] = [1.1, 2.2, 3.3] \n
		driver.sense.listPy.power.sequence.set(structure) \n
		No command help available \n
			:param structure: for set value, see the help for SequenceStruct structure arguments.
		"""
		self._core.io.write_struct(f'SENSe:LIST:POWer:SEQuence', structure)

	def get(self) -> SequenceStruct:
		"""SCPI: [SENSe]:LIST:POWer[:SEQuence] \n
		Snippet: value: SequenceStruct = driver.sense.listPy.power.sequence.get() \n
		No command help available \n
			:return: structure: for return value, see the help for SequenceStruct structure arguments."""
		return self._core.io.query_struct(f'SENSe:LIST:POWer:SEQuence?', self.__class__.SequenceStruct())
