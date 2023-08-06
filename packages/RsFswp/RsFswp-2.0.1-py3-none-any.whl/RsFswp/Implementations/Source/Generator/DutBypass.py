from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DutBypass:
	"""DutBypass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dutBypass", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: SOURce:GENerator:DUTBypass \n
		Snippet: driver.source.generator.dutBypass.set(state = False) \n
		This command turns the DUT bypass on and off. When you turn on the bypass, the application measures the noise
		characteristics of the R&S FSWP. The DUT bypass is available with the optional Signal Source hardware component. \n
			:param state: ON | OFF | 1 | 0
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:GENerator:DUTBypass {param}')

	def get(self) -> bool:
		"""SCPI: SOURce:GENerator:DUTBypass \n
		Snippet: value: bool = driver.source.generator.dutBypass.get() \n
		This command turns the DUT bypass on and off. When you turn on the bypass, the application measures the noise
		characteristics of the R&S FSWP. The DUT bypass is available with the optional Signal Source hardware component. \n
			:return: state: ON | OFF | 1 | 0"""
		response = self._core.io.query_str(f'SOURce:GENerator:DUTBypass?')
		return Conversions.str_to_bool(response)
