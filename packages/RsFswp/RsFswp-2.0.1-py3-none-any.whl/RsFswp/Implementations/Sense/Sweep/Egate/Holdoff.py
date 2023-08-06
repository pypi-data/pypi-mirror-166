from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Holdoff:
	"""Holdoff commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("holdoff", core, parent)

	def set(self, delay_time: float) -> None:
		"""SCPI: [SENSe]:SWEep:EGATe:HOLDoff \n
		Snippet: driver.sense.sweep.egate.holdoff.set(delay_time = 1.0) \n
		This command defines the gate delay time.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurement application.
			- Turn off automatic pulse detection ([SENSe:]SWEep:PULSe:DETection) . \n
			:param delay_time: numeric value Unit: s
		"""
		param = Conversions.decimal_value_to_str(delay_time)
		self._core.io.write(f'SENSe:SWEep:EGATe:HOLDoff {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:SWEep:EGATe:HOLDoff \n
		Snippet: value: float = driver.sense.sweep.egate.holdoff.get() \n
		This command defines the gate delay time.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Optional pulsed phase noise measurement application.
			- Turn off automatic pulse detection ([SENSe:]SWEep:PULSe:DETection) . \n
			:return: delay_time: No help available"""
		response = self._core.io.query_str(f'SENSe:SWEep:EGATe:HOLDoff?')
		return Conversions.str_to_float(response)
