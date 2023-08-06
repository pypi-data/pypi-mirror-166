from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Span:
	"""Span commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("span", core, parent)

	def set(self, span: float) -> None:
		"""SCPI: [SENSe]:CREFerence:PDETect:RANGe:SPAN \n
		Snippet: driver.applications.k50Spurious.sense.creference.pdetect.range.span.set(span = 1.0) \n
		Defines the width of the range in which the maximum peak is searched. \n
			:param span: Unit: HZ
		"""
		param = Conversions.decimal_value_to_str(span)
		self._core.io.write(f'SENSe:CREFerence:PDETect:RANGe:SPAN {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:CREFerence:PDETect:RANGe:SPAN \n
		Snippet: value: float = driver.applications.k50Spurious.sense.creference.pdetect.range.span.get() \n
		Defines the width of the range in which the maximum peak is searched. \n
			:return: span: Unit: HZ"""
		response = self._core.io.query_str(f'SENSe:CREFerence:PDETect:RANGe:SPAN?')
		return Conversions.str_to_float(response)
