from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	def get(self, trace_mode: enums.TraceModeB) -> float:
		"""SCPI: [SENSe]:ADEMod:AM:RELative:AFSPectrum:RESult \n
		Snippet: value: float = driver.sense.ademod.am.relative.afSpectrum.result.get(trace_mode = enums.TraceModeB.AVERage) \n
		This command reads the result data of the evaluated signal in the specified trace mode. The data format of the output
		data block is defined by the FORMat command (see FORMat[:​DATA]) . The trace results are configured for a specific
		evaluation. The following table indicates which command syntax refers to which evaluation method, as well as the output
		unit of the results.
			Table Header: Command syntax / Evaluation method / Output unit \n
			- AM[:ABSolute][:TDOMain] / RF time domain / dBm
			- AM:RELative[:TDOMain] / AM time domain / %
			- AM:RELative:AFSPectrum / AM spectrum / %
			- FM[:TDOMain] / FM time domain / kHz
			- FM:AFSPectrum / FM spectrum / kHz
			- PM[:TDOMain] / PM time domain / rad or °
			- PM:AFSPectrum / PM spectrum / rad or °
			- SPECtrum / RF spectrum / dBm (logarithmic display) or V (linear display) . \n
			:param trace_mode: WRITe | AVERage | MAXHold | MINHold | VIEW The specified trace mode must be one of those configured by SENS:ADEM:Evaluation:TYPE, see [SENSe:​]ADEModn:​SPECtrum[:​TYPE]. Otherwise a query error is generated.
			:return: trace_mode_result: No help available"""
		param = Conversions.enum_scalar_to_str(trace_mode, enums.TraceModeB)
		response = self._core.io.query_str(f'SENSe:ADEMod:AM:RELative:AFSPectrum:RESult? {param}')
		return Conversions.str_to_float(response)
