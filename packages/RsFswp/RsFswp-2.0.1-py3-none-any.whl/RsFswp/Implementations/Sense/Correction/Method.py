from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Method:
	"""Method commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("method", core, parent)

	def set(self, type_py: enums.CorrectionMethod) -> None:
		"""SCPI: [SENSe]:CORRection:METHod \n
		Snippet: driver.sense.correction.method.set(type_py = enums.CorrectionMethod.REFLexion) \n
		No command help available \n
			:param type_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.CorrectionMethod)
		self._core.io.write(f'SENSe:CORRection:METHod {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.CorrectionMethod:
		"""SCPI: [SENSe]:CORRection:METHod \n
		Snippet: value: enums.CorrectionMethod = driver.sense.correction.method.get() \n
		No command help available \n
			:return: type_py: No help available"""
		response = self._core.io.query_str(f'SENSe:CORRection:METHod?')
		return Conversions.str_to_scalar_enum(response, enums.CorrectionMethod)
