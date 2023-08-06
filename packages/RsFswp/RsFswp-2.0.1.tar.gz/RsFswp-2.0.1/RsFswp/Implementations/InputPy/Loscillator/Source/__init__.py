from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def external(self):
		"""external commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_external'):
			from .External import External
			self._external = External(self._core, self._cmd_group)
		return self._external

	def set(self, location: enums.SourceInt, inputIx=repcap.InputIx.Default) -> None:
		"""SCPI: INPut<ip>:LOSCillator:SOURce \n
		Snippet: driver.inputPy.loscillator.source.set(location = enums.SourceInt.EXTernal, inputIx = repcap.InputIx.Default) \n
		This command selects the type of local oscillator in the test setup.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select additive noise or pulsed additive noise measurement (CONFigure:PNOise:MEASurement) . \n
			:param location: EXTernal External local oscillator connected to the 'LO AUX Input' of the R&S FSWP. INTernal Internal local oscillator of the R&S FSWP.
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
		"""
		param = Conversions.enum_scalar_to_str(location, enums.SourceInt)
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		self._core.io.write(f'INPut{inputIx_cmd_val}:LOSCillator:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, inputIx=repcap.InputIx.Default) -> enums.SourceInt:
		"""SCPI: INPut<ip>:LOSCillator:SOURce \n
		Snippet: value: enums.SourceInt = driver.inputPy.loscillator.source.get(inputIx = repcap.InputIx.Default) \n
		This command selects the type of local oscillator in the test setup.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select additive noise or pulsed additive noise measurement (CONFigure:PNOise:MEASurement) . \n
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
			:return: location: EXTernal External local oscillator connected to the 'LO AUX Input' of the R&S FSWP. INTernal Internal local oscillator of the R&S FSWP."""
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		response = self._core.io.query_str(f'INPut{inputIx_cmd_val}:LOSCillator:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def clone(self) -> 'Source':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Source(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
