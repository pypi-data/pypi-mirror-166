from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.EgateType) -> None:
		"""SCPI: [SENSe]:SWEep:EGATe:TYPE \n
		Snippet: driver.sense.sweep.egate.typePy.set(type_py = enums.EgateType.EDGE) \n
		This command selects the gate type.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurement application. \n
			:param type_py: EDGE The gate opens when the gate level has been exceeded and closes when the time defined by the gate length has elapsed. LEVel The gate opens when the gate level has been exceeded and closes when the signal level again falls below the gate level. OFF The gate is off.
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.EgateType)
		self._core.io.write(f'SENSe:SWEep:EGATe:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.EgateType:
		"""SCPI: [SENSe]:SWEep:EGATe:TYPE \n
		Snippet: value: enums.EgateType = driver.sense.sweep.egate.typePy.get() \n
		This command selects the gate type.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurement application. \n
			:return: type_py: No help available"""
		response = self._core.io.query_str(f'SENSe:SWEep:EGATe:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.EgateType)
