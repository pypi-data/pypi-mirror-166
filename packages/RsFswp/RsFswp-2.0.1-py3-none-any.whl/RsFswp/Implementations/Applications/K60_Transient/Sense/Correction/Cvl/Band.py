from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Band:
	"""Band commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("band", core, parent)

	def set(self, band: enums.BandB) -> None:
		"""SCPI: [SENSe]:CORRection:CVL:BAND \n
		Snippet: driver.applications.k60Transient.sense.correction.cvl.band.set(band = enums.BandB.D) \n
		No command help available \n
			:param band: No help available
		"""
		param = Conversions.enum_scalar_to_str(band, enums.BandB)
		self._core.io.write(f'SENSe:CORRection:CVL:BAND {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.BandB:
		"""SCPI: [SENSe]:CORRection:CVL:BAND \n
		Snippet: value: enums.BandB = driver.applications.k60Transient.sense.correction.cvl.band.get() \n
		No command help available \n
			:return: band: No help available"""
		response = self._core.io.query_str(f'SENSe:CORRection:CVL:BAND?')
		return Conversions.str_to_scalar_enum(response, enums.BandB)
