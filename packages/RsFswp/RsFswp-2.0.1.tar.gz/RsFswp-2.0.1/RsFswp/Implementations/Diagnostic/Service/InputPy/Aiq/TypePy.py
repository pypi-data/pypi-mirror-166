from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, signal_type: enums.SignalType) -> None:
		"""SCPI: DIAGnostic:SERVice:INPut:AIQ[:TYPE] \n
		Snippet: driver.diagnostic.service.inputPy.aiq.typePy.set(signal_type = enums.SignalType.AC) \n
		No command help available \n
			:param signal_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(signal_type, enums.SignalType)
		self._core.io.write(f'DIAGnostic:SERVice:INPut:AIQ:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.SignalType:
		"""SCPI: DIAGnostic:SERVice:INPut:AIQ[:TYPE] \n
		Snippet: value: enums.SignalType = driver.diagnostic.service.inputPy.aiq.typePy.get() \n
		No command help available \n
			:return: signal_type: No help available"""
		response = self._core.io.query_str(f'DIAGnostic:SERVice:INPut:AIQ:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.SignalType)
