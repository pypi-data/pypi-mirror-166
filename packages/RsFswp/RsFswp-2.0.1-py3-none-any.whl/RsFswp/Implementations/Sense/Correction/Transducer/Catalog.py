from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("catalog", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Used_Disk_Space: int: No parameter help available
			- Free_Disk_Space: int: No parameter help available
			- File_Size: List[int]: No parameter help available
			- Filename: List[str]: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Used_Disk_Space'),
			ArgStruct.scalar_int('Free_Disk_Space'),
			ArgStruct('File_Size', DataType.IntegerList, None, False, True, 1),
			ArgStruct('Filename', DataType.StringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Used_Disk_Space: int = None
			self.Free_Disk_Space: int = None
			self.File_Size: List[int] = None
			self.Filename: List[str] = None

	def get(self) -> GetStruct:
		"""SCPI: [SENSe]:CORRection:TRANsducer:CATalog \n
		Snippet: value: GetStruct = driver.sense.correction.transducer.catalog.get() \n
		No command help available \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SENSe:CORRection:TRANsducer:CATalog?', self.__class__.GetStruct())
