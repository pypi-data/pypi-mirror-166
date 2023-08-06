from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.SweepModeC) -> None:
		"""SCPI: [SENSe]:SWEep:MODE \n
		Snippet: driver.sense.sweep.mode.set(mode = enums.SweepModeC.AUTO) \n
		This command selects the configuration mode of the half decade table. \n
			:param mode: MANual Manual mode: allows you to select a custom resolution bandwidth and number of cross-correlations for each half decade. • Define the RBW for a half decade with [SENSe:]LIST:RANGer:BWIDth[:RESolution]. • Define the number of cross-correlations for a half decade with [SENSe:]LIST:RANGer:XCOunt. NORMal Automatic mode: the application selects the resolution bandwidth and number of cross-correlations based on the RBW and XCORR factors. • Define the RBW factor with [SENSe:]LIST:BWIDth[:RESolution]:RATio. • Define the XCORR factor with [SENSe:]SWEep:XFACtor.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.SweepModeC)
		self._core.io.write(f'SENSe:SWEep:MODE {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.SweepModeC:
		"""SCPI: [SENSe]:SWEep:MODE \n
		Snippet: value: enums.SweepModeC = driver.sense.sweep.mode.get() \n
		This command selects the configuration mode of the half decade table. \n
			:return: mode: MANual Manual mode: allows you to select a custom resolution bandwidth and number of cross-correlations for each half decade. • Define the RBW for a half decade with [SENSe:]LIST:RANGer:BWIDth[:RESolution]. • Define the number of cross-correlations for a half decade with [SENSe:]LIST:RANGer:XCOunt. NORMal Automatic mode: the application selects the resolution bandwidth and number of cross-correlations based on the RBW and XCORR factors. • Define the RBW factor with [SENSe:]LIST:BWIDth[:RESolution]:RATio. • Define the XCORR factor with [SENSe:]SWEep:XFACtor."""
		response = self._core.io.query_str(f'SENSe:SWEep:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SweepModeC)
