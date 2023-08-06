from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Set:
	"""Set commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("set", core, parent)

	# noinspection PyTypeChecker
	class SetStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- State_Peak: bool: No parameter help available
			- State_Rms: bool: No parameter help available
			- State_Avg: bool: No parameter help available
			- Trigger_Source: enums.TriggerSourceListPower: No parameter help available
			- Trigger_Slope: enums.SlopeType: No parameter help available
			- Trigger_Offset: float: No parameter help available
			- Gate_Length: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('State_Peak'),
			ArgStruct.scalar_bool('State_Rms'),
			ArgStruct.scalar_bool('State_Avg'),
			ArgStruct.scalar_enum('Trigger_Source', enums.TriggerSourceListPower),
			ArgStruct.scalar_enum('Trigger_Slope', enums.SlopeType),
			ArgStruct.scalar_float('Trigger_Offset'),
			ArgStruct.scalar_float('Gate_Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.State_Peak: bool = None
			self.State_Rms: bool = None
			self.State_Avg: bool = None
			self.Trigger_Source: enums.TriggerSourceListPower = None
			self.Trigger_Slope: enums.SlopeType = None
			self.Trigger_Offset: float = None
			self.Gate_Length: float = None

	def set(self, structure: SetStruct) -> None:
		"""SCPI: [SENSe]:LIST:POWer:SET \n
		Snippet with structure: \n
		structure = driver.sense.listPy.power.set.SetStruct() \n
		structure.State_Peak: bool = False \n
		structure.State_Rms: bool = False \n
		structure.State_Avg: bool = False \n
		structure.Trigger_Source: enums.TriggerSourceListPower = enums.TriggerSourceListPower.EXT2 \n
		structure.Trigger_Slope: enums.SlopeType = enums.SlopeType.NEGative \n
		structure.Trigger_Offset: float = 1.0 \n
		structure.Gate_Length: float = 1.0 \n
		driver.sense.listPy.power.set.set(structure) \n
		No command help available \n
			:param structure: for set value, see the help for SetStruct structure arguments.
		"""
		self._core.io.write_struct(f'SENSe:LIST:POWer:SET', structure)

	def get(self) -> SetStruct:
		"""SCPI: [SENSe]:LIST:POWer:SET \n
		Snippet: value: SetStruct = driver.sense.listPy.power.set.get() \n
		No command help available \n
			:return: structure: for return value, see the help for SetStruct structure arguments."""
		return self._core.io.query_struct(f'SENSe:LIST:POWer:SET?', self.__class__.SetStruct())
