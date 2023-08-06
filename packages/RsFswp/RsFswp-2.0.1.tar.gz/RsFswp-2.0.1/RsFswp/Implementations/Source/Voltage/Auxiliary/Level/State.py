from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: SOURce:VOLTage:AUX:LEVel[:STATe] \n
		Snippet: driver.source.voltage.auxiliary.level.state.set(state = False) \n
		This command turns the auxiliary voltage source (Vaux) on and off. Note that DC power is actually supplied only if you
		additionally activate the outputs in general.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on DC power sources (method RsFswp.Source.Voltage.State.set) . \n
			:param state: ON | OFF | 1 | 0
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:VOLTage:AUX:LEVel:STATe {param}')

	def get(self) -> bool:
		"""SCPI: SOURce:VOLTage:AUX:LEVel[:STATe] \n
		Snippet: value: bool = driver.source.voltage.auxiliary.level.state.get() \n
		This command turns the auxiliary voltage source (Vaux) on and off. Note that DC power is actually supplied only if you
		additionally activate the outputs in general.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Turn on DC power sources (method RsFswp.Source.Voltage.State.set) . \n
			:return: state: ON | OFF | 1 | 0"""
		response = self._core.io.query_str(f'SOURce:VOLTage:AUX:LEVel:STATe?')
		return Conversions.str_to_bool(response)
