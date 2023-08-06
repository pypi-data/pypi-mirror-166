from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, source: enums.InputSource, inputIx=repcap.InputIx.Default) -> None:
		"""SCPI: INPut<ip>:SELect \n
		Snippet: driver.inputPy.select.set(source = enums.InputSource.ABBand, inputIx = repcap.InputIx.Default) \n
		This command selects the signal source for measurements, i.e. it defines which connector is used to input data to the R&S
		FSWP. \n
			:param source: RF Radio Frequency ('RF INPUT' connector) FIQ I/Q data file (selected by method RsFswp.InputPy.File.Path.set) For details see 'Basics on Input from I/Q Data Files'.
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InputPy')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.InputSource)
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		self._core.io.write(f'INPut{inputIx_cmd_val}:SELect {param}')
