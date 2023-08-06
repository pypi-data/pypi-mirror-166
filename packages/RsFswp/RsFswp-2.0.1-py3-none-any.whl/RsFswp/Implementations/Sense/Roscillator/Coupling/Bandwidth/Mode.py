from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.AutoManualMode) -> None:
		"""SCPI: [SENSe]:ROSCillator:COUPling:BANDwidth:MODE \n
		Snippet: driver.sense.roscillator.coupling.bandwidth.mode.set(mode = enums.AutoManualMode.AUTO) \n
		This command selects coupling bandwidth mode for the internal reference frequency.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Options R&S FSWP-B60 or -B61 must be available. \n
			:param mode: AUTO Automatically selects an appropriate coupling bandwidth. MANual Manual selection of coupling bandwidth. You can select the bandwidth with [SENSe:]ROSCillator:COUPling:BANDwidth.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AutoManualMode)
		self._core.io.write(f'SENSe:ROSCillator:COUPling:BANDwidth:MODE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.AutoManualMode:
		"""SCPI: [SENSe]:ROSCillator:COUPling:BANDwidth:MODE \n
		Snippet: value: enums.AutoManualMode = driver.sense.roscillator.coupling.bandwidth.mode.get() \n
		This command selects coupling bandwidth mode for the internal reference frequency.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Options R&S FSWP-B60 or -B61 must be available. \n
			:return: mode: AUTO Automatically selects an appropriate coupling bandwidth. MANual Manual selection of coupling bandwidth. You can select the bandwidth with [SENSe:]ROSCillator:COUPling:BANDwidth."""
		response = self._core.io.query_str(f'SENSe:ROSCillator:COUPling:BANDwidth:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)
