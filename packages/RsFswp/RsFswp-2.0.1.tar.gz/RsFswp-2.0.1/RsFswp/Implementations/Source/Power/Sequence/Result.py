from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Power_Vsupply: float: No parameter help available
			- Power_Vtune: float: No parameter help available
			- Power_Vaux: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Power_Vsupply'),
			ArgStruct.scalar_float('Power_Vtune'),
			ArgStruct.scalar_float('Power_Vaux')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power_Vsupply: float = None
			self.Power_Vtune: float = None
			self.Power_Vaux: float = None

	def get(self) -> GetStruct:
		"""SCPI: SOURce:POWer:SEQuence:RESult \n
		Snippet: value: GetStruct = driver.source.power.sequence.result.get() \n
		This command queries the actually measured power (U*I) on the DC power sources.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on DC power sources (method RsFswp.Source.Voltage.State.set) . \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:POWer:SEQuence:RESult?', self.__class__.GetStruct())
