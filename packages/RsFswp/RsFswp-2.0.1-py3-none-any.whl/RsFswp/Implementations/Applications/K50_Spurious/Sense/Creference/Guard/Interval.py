from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interval:
	"""Interval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("interval", core, parent)

	def set(self, span: float) -> None:
		"""SCPI: [SENSe]:CREFerence:GUARd:INTerval \n
		Snippet: driver.applications.k50Spurious.sense.creference.guard.interval.set(span = 1.0) \n
		Defines the guard interval as a span around the reference carrier.
		This setting is only available for [SENSe:]CREFerence:GUARd:STATe OFF \n
			:param span: Unit: HZ
		"""
		param = Conversions.decimal_value_to_str(span)
		self._core.io.write(f'SENSe:CREFerence:GUARd:INTerval {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:CREFerence:GUARd:INTerval \n
		Snippet: value: float = driver.applications.k50Spurious.sense.creference.guard.interval.get() \n
		Defines the guard interval as a span around the reference carrier.
		This setting is only available for [SENSe:]CREFerence:GUARd:STATe OFF \n
			:return: span: Unit: HZ"""
		response = self._core.io.query_str(f'SENSe:CREFerence:GUARd:INTerval?')
		return Conversions.str_to_float(response)
