from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Threshold:
	"""Threshold commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("threshold", core, parent)

	def set(self, level: float) -> None:
		"""SCPI: [SENSe]:ADJust:CONFigure:LEVel:THReshold \n
		Snippet: driver.sense.adjust.configure.level.threshold.set(level = 1.0) \n
		This command defines the threshold of the signal search.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on the automatic signal search with [SENSe:]ADJust:CONFigure:FREQuency:AUTosearch[:STATe] \n
			:param level: numeric value Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SENSe:ADJust:CONFigure:LEVel:THReshold {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:ADJust:CONFigure:LEVel:THReshold \n
		Snippet: value: float = driver.sense.adjust.configure.level.threshold.get() \n
		This command defines the threshold of the signal search.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on the automatic signal search with [SENSe:]ADJust:CONFigure:FREQuency:AUTosearch[:STATe] \n
			:return: level: numeric value Unit: dBm"""
		response = self._core.io.query_str(f'SENSe:ADJust:CONFigure:LEVel:THReshold?')
		return Conversions.str_to_float(response)
