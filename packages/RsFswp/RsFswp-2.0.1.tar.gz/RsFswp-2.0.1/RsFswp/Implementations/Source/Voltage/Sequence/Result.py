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
			- Voltage_Vsupply: float: No parameter help available
			- Voltage_Vtune: float: No parameter help available
			- Voltage_Vaux: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Voltage_Vsupply'),
			ArgStruct.scalar_float('Voltage_Vtune'),
			ArgStruct.scalar_float('Voltage_Vaux')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Voltage_Vsupply: float = None
			self.Voltage_Vtune: float = None
			self.Voltage_Vaux: float = None

	def get(self) -> GetStruct:
		"""SCPI: SOURce:VOLTage:SEQuence:RESult \n
		Snippet: value: GetStruct = driver.source.voltage.sequence.result.get() \n
		This command queries the actually measured voltages on the DC power sources.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on DC power sources (method RsFswp.Source.Voltage.State.set) . \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:VOLTage:SEQuence:RESult?', self.__class__.GetStruct())
