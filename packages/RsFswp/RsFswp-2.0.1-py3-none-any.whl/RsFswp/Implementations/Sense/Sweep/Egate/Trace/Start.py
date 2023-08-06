from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Start:
	"""Start commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("start", core, parent)

	def set(self, time: float, trace=repcap.Trace.Default, gateRange=repcap.GateRange.Nr1) -> None:
		"""SCPI: [SENSe]:SWEep:EGATe:TRACe<t>:STARt<gr> \n
		Snippet: driver.sense.sweep.egate.trace.start.set(time = 1.0, trace = repcap.Trace.Default, gateRange = repcap.GateRange.Nr1) \n
		No command help available \n
			:param time: No help available
			:param trace: optional repeated capability selector. Default value: Tr1 (settable in the interface 'Trace')
			:param gateRange: optional repeated capability selector. Default value: Nr1
		"""
		param = Conversions.decimal_value_to_str(time)
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		gateRange_cmd_val = self._cmd_group.get_repcap_cmd_value(gateRange, repcap.GateRange)
		self._core.io.write(f'SENSe:SWEep:EGATe:TRACe{trace_cmd_val}:STARt{gateRange_cmd_val} {param}')

	def get(self, trace=repcap.Trace.Default, gateRange=repcap.GateRange.Nr1) -> float:
		"""SCPI: [SENSe]:SWEep:EGATe:TRACe<t>:STARt<gr> \n
		Snippet: value: float = driver.sense.sweep.egate.trace.start.get(trace = repcap.Trace.Default, gateRange = repcap.GateRange.Nr1) \n
		No command help available \n
			:param trace: optional repeated capability selector. Default value: Tr1 (settable in the interface 'Trace')
			:param gateRange: optional repeated capability selector. Default value: Nr1
			:return: time: No help available"""
		trace_cmd_val = self._cmd_group.get_repcap_cmd_value(trace, repcap.Trace)
		gateRange_cmd_val = self._cmd_group.get_repcap_cmd_value(gateRange, repcap.GateRange)
		response = self._core.io.query_str(f'SENSe:SWEep:EGATe:TRACe{trace_cmd_val}:STARt{gateRange_cmd_val}?')
		return Conversions.str_to_float(response)
