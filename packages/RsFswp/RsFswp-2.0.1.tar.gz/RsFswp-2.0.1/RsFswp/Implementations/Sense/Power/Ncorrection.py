from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ncorrection:
	"""Ncorrection commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ncorrection", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: [SENSe]:POWer:NCORrection \n
		Snippet: driver.sense.power.ncorrection.set(state = False) \n
		This command turns noise cancellation on and off. If noise cancellation is on, the R&S FSWP performs a reference
		measurement to determine its inherent noise and subtracts the result from the channel power measurement result (first
		active trace only) . For more information see 'Noise Cancellation'. \n
			:param state: ON | OFF | 1 | 0
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SENSe:POWer:NCORrection {param}')

	def get(self) -> bool:
		"""SCPI: [SENSe]:POWer:NCORrection \n
		Snippet: value: bool = driver.sense.power.ncorrection.get() \n
		This command turns noise cancellation on and off. If noise cancellation is on, the R&S FSWP performs a reference
		measurement to determine its inherent noise and subtracts the result from the channel power measurement result (first
		active trace only) . For more information see 'Noise Cancellation'. \n
			:return: state: ON | OFF | 1 | 0"""
		response = self._core.io.query_str(f'SENSe:POWer:NCORrection?')
		return Conversions.str_to_bool(response)
