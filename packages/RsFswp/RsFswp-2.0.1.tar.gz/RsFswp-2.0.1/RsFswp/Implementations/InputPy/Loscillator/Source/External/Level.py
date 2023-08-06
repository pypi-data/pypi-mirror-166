from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level: enums.LowHigh, inputIx=repcap.InputIx.Default) -> None:
		"""SCPI: INPut<ip>:LOSCillator:SOURce:EXTernal:LEVel \n
		Snippet: driver.inputPy.loscillator.source.external.level.set(level = enums.LowHigh.HIGH, inputIx = repcap.InputIx.Default) \n
		This command selects the level of an external LO signal that is fed into the R&S FSWP.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select additive noise or pulsed additive noise measurement (CONFigure:PNOise:MEASurement) .
			- Select an external local oscillator (method RsFswp.InputPy.Loscillator.Source.set) . \n
			:param level: HIGH LO signal with high level characteristics. LOW LO signal with low level characteristics.
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
		"""
		param = Conversions.enum_scalar_to_str(level, enums.LowHigh)
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		self._core.io.write(f'INPut{inputIx_cmd_val}:LOSCillator:SOURce:EXTernal:LEVel {param}')

	# noinspection PyTypeChecker
	def get(self, inputIx=repcap.InputIx.Default) -> enums.LowHigh:
		"""SCPI: INPut<ip>:LOSCillator:SOURce:EXTernal:LEVel \n
		Snippet: value: enums.LowHigh = driver.inputPy.loscillator.source.external.level.get(inputIx = repcap.InputIx.Default) \n
		This command selects the level of an external LO signal that is fed into the R&S FSWP.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Select additive noise or pulsed additive noise measurement (CONFigure:PNOise:MEASurement) .
			- Select an external local oscillator (method RsFswp.InputPy.Loscillator.Source.set) . \n
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
			:return: level: HIGH LO signal with high level characteristics. LOW LO signal with low level characteristics."""
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		response = self._core.io.query_str(f'INPut{inputIx_cmd_val}:LOSCillator:SOURce:EXTernal:LEVel?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)
