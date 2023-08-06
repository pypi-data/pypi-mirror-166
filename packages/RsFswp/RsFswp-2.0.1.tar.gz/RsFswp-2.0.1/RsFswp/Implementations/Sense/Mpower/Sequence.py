from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sequence", core, parent)

	# noinspection PyTypeChecker
	class SetStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Frequency: float: No parameter help available
			- Rbw: float: No parameter help available
			- Meas_Time: float: No parameter help available
			- Trigger_Source: enums.TriggerSourceMpower: No parameter help available
			- Trigger_Level: float: No parameter help available
			- Trigger_Offset: float: No parameter help available
			- Detector: enums.MpowerDetector: No parameter help available
			- Of_Pulses: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_float('Rbw'),
			ArgStruct.scalar_float('Meas_Time'),
			ArgStruct.scalar_enum('Trigger_Source', enums.TriggerSourceMpower),
			ArgStruct.scalar_float('Trigger_Level'),
			ArgStruct.scalar_float('Trigger_Offset'),
			ArgStruct.scalar_enum('Detector', enums.MpowerDetector),
			ArgStruct.scalar_float('Of_Pulses')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency: float = None
			self.Rbw: float = None
			self.Meas_Time: float = None
			self.Trigger_Source: enums.TriggerSourceMpower = None
			self.Trigger_Level: float = None
			self.Trigger_Offset: float = None
			self.Detector: enums.MpowerDetector = None
			self.Of_Pulses: float = None

	def set(self, structure: SetStruct) -> None:
		"""SCPI: [SENSe]:MPOWer[:SEQuence] \n
		Snippet with structure: \n
		structure = driver.sense.mpower.sequence.SetStruct() \n
		structure.Frequency: float = 1.0 \n
		structure.Rbw: float = 1.0 \n
		structure.Meas_Time: float = 1.0 \n
		structure.Trigger_Source: enums.TriggerSourceMpower = enums.TriggerSourceMpower.EXT2 \n
		structure.Trigger_Level: float = 1.0 \n
		structure.Trigger_Offset: float = 1.0 \n
		structure.Detector: enums.MpowerDetector = enums.MpowerDetector.MEAN \n
		structure.Of_Pulses: float = 1.0 \n
		driver.sense.mpower.sequence.set(structure) \n
		No command help available \n
			:param structure: for set value, see the help for SetStruct structure arguments.
		"""
		self._core.io.write_struct(f'SENSe:MPOWer:SEQuence', structure)

	def get(self) -> List[float]:
		"""SCPI: [SENSe]:MPOWer[:SEQuence] \n
		Snippet: value: List[float] = driver.sense.mpower.sequence.get() \n
		No command help available \n
			:return: power_levels: No help available"""
		response = self._core.io.query_bin_or_ascii_float_list(f'SENSe:MPOWer:SEQuence?')
		return response
