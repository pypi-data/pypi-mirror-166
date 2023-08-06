from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool) -> None:
		"""SCPI: SOURce:VOLTage[:STATe] \n
		Snippet: driver.source.voltage.state.set(state = False) \n
		This command turns DC power sources on and off in general. When you turn off the DC power sources, no power is supplied
		even when you have turned on one of the sources individually with one of the following commands.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- method RsFswp.Source.Voltage.Auxiliary.Level.State.set
			- method RsFswp.Applications.K30_NoiseFigure.Source.Voltage.Control.Level.State.set
			- method RsFswp.Applications.K30_NoiseFigure.Source.Voltage.Power.Level.State.set
		Note that you can turn on the global power supply if at least one of the individual supplies has been turned on. \n
			:param state: ON | 1 DC power sources are ready for use. OFF | 0 DC power sources are turned off.
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:VOLTage:STATe {param}')

	def get(self) -> bool:
		"""SCPI: SOURce:VOLTage[:STATe] \n
		Snippet: value: bool = driver.source.voltage.state.get() \n
		This command turns DC power sources on and off in general. When you turn off the DC power sources, no power is supplied
		even when you have turned on one of the sources individually with one of the following commands.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- method RsFswp.Source.Voltage.Auxiliary.Level.State.set
			- method RsFswp.Applications.K30_NoiseFigure.Source.Voltage.Control.Level.State.set
			- method RsFswp.Applications.K30_NoiseFigure.Source.Voltage.Power.Level.State.set
		Note that you can turn on the global power supply if at least one of the individual supplies has been turned on. \n
			:return: state: ON | 1 DC power sources are ready for use. OFF | 0 DC power sources are turned off."""
		response = self._core.io.query_str(f'SOURce:VOLTage:STATe?')
		return Conversions.str_to_bool(response)
