from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RefLevel:
	"""RefLevel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("refLevel", core, parent)

	def set(self, state: enums.Synchronization) -> None:
		"""SCPI: INSTrument:COUPle:RLEVel \n
		Snippet: driver.instrument.couple.refLevel.set(state = enums.Synchronization.ALL) \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.enum_scalar_to_str(state, enums.Synchronization)
		self._core.io.write(f'INSTrument:COUPle:RLEVel {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.Synchronization:
		"""SCPI: INSTrument:COUPle:RLEVel \n
		Snippet: value: enums.Synchronization = driver.instrument.couple.refLevel.get() \n
		No command help available \n
			:return: state: No help available"""
		response = self._core.io.query_str(f'INSTrument:COUPle:RLEVel?')
		return Conversions.str_to_scalar_enum(response, enums.Synchronization)
