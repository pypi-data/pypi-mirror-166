from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.PwrLevelMode, source=repcap.Source.Default) -> None:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LEVel:MODE \n
		Snippet: driver.source.voltage.power.level.mode.set(mode = enums.PwrLevelMode.CURRent, source = repcap.Source.Default) \n
		This command selects whether you want to control the output in terms of current or voltage. \n
			:param mode: CURRent Control the output in terms of current. VOLTage Controls the output in terms of voltage.
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PwrLevelMode)
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		self._core.io.write(f'SOURce:VOLTage:POWer{source_cmd_val}:LEVel:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, source=repcap.Source.Default) -> enums.PwrLevelMode:
		"""SCPI: SOURce:VOLTage:POWer<1|2>:LEVel:MODE \n
		Snippet: value: enums.PwrLevelMode = driver.source.voltage.power.level.mode.get(source = repcap.Source.Default) \n
		This command selects whether you want to control the output in terms of current or voltage. \n
			:param source: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: mode: CURRent Control the output in terms of current. VOLTage Controls the output in terms of voltage."""
		source_cmd_val = self._cmd_group.get_repcap_cmd_value(source, repcap.Source)
		response = self._core.io.query_str(f'SOURce:VOLTage:POWer{source_cmd_val}:LEVel:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PwrLevelMode)
