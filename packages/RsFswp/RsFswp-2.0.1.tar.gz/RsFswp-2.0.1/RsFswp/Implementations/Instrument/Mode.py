from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, op_mode: enums.InstrumentMode) -> None:
		"""SCPI: INSTrument:MODE \n
		Snippet: driver.instrument.mode.set(op_mode = enums.InstrumentMode.MSRanalyzer) \n
		No command help available \n
			:param op_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(op_mode, enums.InstrumentMode)
		self._core.io.write_with_opc(f'INSTrument:MODE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.InstrumentMode:
		"""SCPI: INSTrument:MODE \n
		Snippet: value: enums.InstrumentMode = driver.instrument.mode.get() \n
		No command help available \n
			:return: op_mode: No help available"""
		response = self._core.io.query_str_with_opc(f'INSTrument:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.InstrumentMode)
