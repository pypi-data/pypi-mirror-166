from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class High:
	"""High commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("high", core, parent)

	def set(self, frequency: float) -> None:
		"""SCPI: [SENSe]:ADJust:CONFigure:FREQuency:LIMit:HIGH \n
		Snippet: driver.sense.adjust.configure.frequency.limit.high.set(frequency = 1.0) \n
		This command defines the upper limit of the frequency search range.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on the automatic signal search with [SENSe:]ADJust:CONFigure:FREQuency:AUTosearch[:STATe] \n
			:param frequency: numeric value Range: See data sheet , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SENSe:ADJust:CONFigure:FREQuency:LIMit:HIGH {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:ADJust:CONFigure:FREQuency:LIMit:HIGH \n
		Snippet: value: float = driver.sense.adjust.configure.frequency.limit.high.get() \n
		This command defines the upper limit of the frequency search range.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on the automatic signal search with [SENSe:]ADJust:CONFigure:FREQuency:AUTosearch[:STATe] \n
			:return: frequency: numeric value Range: See data sheet , Unit: Hz"""
		response = self._core.io.query_str(f'SENSe:ADJust:CONFigure:FREQuency:LIMit:HIGH?')
		return Conversions.str_to_float(response)
