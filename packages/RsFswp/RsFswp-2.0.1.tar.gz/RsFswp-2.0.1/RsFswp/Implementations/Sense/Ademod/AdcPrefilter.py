from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdcPrefilter:
	"""AdcPrefilter commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("adcPrefilter", core, parent)

	def set(self, mode: enums.AdcPreFilterMode) -> None:
		"""SCPI: [SENSe]:ADEMod:ADCPrefilter \n
		Snippet: driver.sense.ademod.adcPrefilter.set(mode = enums.AdcPreFilterMode.AUTO) \n
		This command selects the bandwidth selection mode for the ADC prefilter. \n
			:param mode: AUTO Selects the analog bandwidth based on the demodulation bandwidth. WIDE Selects the largest possible analog bandwidth.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AdcPreFilterMode)
		self._core.io.write(f'SENSe:ADEMod:ADCPrefilter {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.AdcPreFilterMode:
		"""SCPI: [SENSe]:ADEMod:ADCPrefilter \n
		Snippet: value: enums.AdcPreFilterMode = driver.sense.ademod.adcPrefilter.get() \n
		This command selects the bandwidth selection mode for the ADC prefilter. \n
			:return: mode: AUTO Selects the analog bandwidth based on the demodulation bandwidth. WIDE Selects the largest possible analog bandwidth."""
		response = self._core.io.query_str(f'SENSe:ADEMod:ADCPrefilter?')
		return Conversions.str_to_scalar_enum(response, enums.AdcPreFilterMode)
