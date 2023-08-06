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
			- Current_Vsupply: float: No parameter help available
			- Current_Vtune: float: No parameter help available
			- Current_Vaux: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Current_Vsupply'),
			ArgStruct.scalar_float('Current_Vtune'),
			ArgStruct.scalar_float('Current_Vaux')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Current_Vsupply: float = None
			self.Current_Vtune: float = None
			self.Current_Vaux: float = None

	def get(self) -> GetStruct:
		"""SCPI: SOURce:CURRent:SEQuence:RESult \n
		Snippet: value: GetStruct = driver.source.current.sequence.result.get() \n
		This command queries the actually measured current on the DC power sources.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on the DC power source (method RsFswp.Source.Voltage.State.set) . \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:CURRent:SEQuence:RESult?', self.__class__.GetStruct())
