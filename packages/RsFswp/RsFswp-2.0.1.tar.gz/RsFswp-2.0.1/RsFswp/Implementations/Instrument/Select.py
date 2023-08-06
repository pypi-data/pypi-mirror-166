from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, channel_type: enums.ChannelType) -> None:
		"""SCPI: INSTrument[:SELect] \n
		Snippet: driver.instrument.select.set(channel_type = enums.ChannelType.IqAnalyzer=IQ) \n
		This command activates a new channel with the defined channel type, or selects an existing channel with the specified
		name. Also see
			INTRO_CMD_HELP: See also \n
			- method RsFswp.Instrument.Create.New.set
			- 'Programming Example: Performing a Sequence of Measurements' \n
			:param channel_type: (enum or string) Channel type of the new channel. For a list of available channel types see method RsFswp.Instrument.ListPy.get_.
		"""
		param = Conversions.enum_ext_scalar_to_str(channel_type, enums.ChannelType)
		self._core.io.write_with_opc(f'INSTrument:SELect {param}')
