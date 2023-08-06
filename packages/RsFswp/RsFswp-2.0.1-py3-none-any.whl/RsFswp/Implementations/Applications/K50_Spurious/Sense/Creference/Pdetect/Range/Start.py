from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Start:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def set(self, start: float) -> None:
		"""SCPI: [SENSe]:CREFerence:PDETect:RANGe:STARt \n
		Snippet: driver.applications.k50Spurious.sense.creference.pdetect.range.start.set(start = 1.0) \n
		Defines the beginning of the range in which the maximum peak is searched. \n
			:param start: Unit: HZ
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SENSe:CREFerence:PDETect:RANGe:STARt {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:CREFerence:PDETect:RANGe:STARt \n
		Snippet: value: float = driver.applications.k50Spurious.sense.creference.pdetect.range.start.get() \n
		Defines the beginning of the range in which the maximum peak is searched. \n
			:return: start: Unit: HZ"""
		response = self._core.io.query_str(f'SENSe:CREFerence:PDETect:RANGe:STARt?')
		return Conversions.str_to_float(response)
