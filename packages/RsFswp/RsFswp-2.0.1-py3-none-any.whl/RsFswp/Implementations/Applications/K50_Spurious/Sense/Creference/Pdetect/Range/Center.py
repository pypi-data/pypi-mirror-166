from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Center:
	"""Center commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("center", core, parent)

	def set(self, center: float) -> None:
		"""SCPI: [SENSe]:CREFerence:PDETect:RANGe:CENTer \n
		Snippet: driver.applications.k50Spurious.sense.creference.pdetect.range.center.set(center = 1.0) \n
		Defines the center of the range in which the maximum peak is searched. \n
			:param center: Unit: HZ
		"""
		param = Conversions.decimal_value_to_str(center)
		self._core.io.write(f'SENSe:CREFerence:PDETect:RANGe:CENTer {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:CREFerence:PDETect:RANGe:CENTer \n
		Snippet: value: float = driver.applications.k50Spurious.sense.creference.pdetect.range.center.get() \n
		Defines the center of the range in which the maximum peak is searched. \n
			:return: center: Unit: HZ"""
		response = self._core.io.query_str(f'SENSe:CREFerence:PDETect:RANGe:CENTer?')
		return Conversions.str_to_float(response)
