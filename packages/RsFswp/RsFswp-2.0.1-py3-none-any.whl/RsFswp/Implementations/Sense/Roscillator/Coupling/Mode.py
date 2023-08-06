from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, state: enums.AutoMode) -> None:
		"""SCPI: [SENSe]:ROSCillator:COUPling:MODE \n
		Snippet: driver.sense.roscillator.coupling.mode.set(state = enums.AutoMode.AUTO) \n
		This command turns the coupling of the internal reference frequency on and off.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Options R&S FSWP-B60 or -B61 must be available. \n
			:param state: AUTO Automatically turns the coupling on and off, depending on the current measurement scenario. OFF Decouples the reference frequencies. ON Couples the reference frequencies.
		"""
		param = Conversions.enum_scalar_to_str(state, enums.AutoMode)
		self._core.io.write(f'SENSe:ROSCillator:COUPling:MODE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.AutoMode:
		"""SCPI: [SENSe]:ROSCillator:COUPling:MODE \n
		Snippet: value: enums.AutoMode = driver.sense.roscillator.coupling.mode.get() \n
		This command turns the coupling of the internal reference frequency on and off.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Options R&S FSWP-B60 or -B61 must be available. \n
			:return: state: AUTO Automatically turns the coupling on and off, depending on the current measurement scenario. OFF Decouples the reference frequencies. ON Couples the reference frequencies."""
		response = self._core.io.query_str(f'SENSe:ROSCillator:COUPling:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoMode)
