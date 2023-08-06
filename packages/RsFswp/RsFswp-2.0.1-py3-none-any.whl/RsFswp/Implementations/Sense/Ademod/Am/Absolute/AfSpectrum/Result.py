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
		"""SCPI: [SENSe]:ADEMod:AM[:ABSolute]:AFSPectrum:RESult \n
		Snippet: value: float = driver.sense.ademod.am.absolute.afSpectrum.result.get(trace_mode = enums.TraceModeB.AVERage) \n
		No command help available \n
			:param trace_mode: No help available
			:return: trace_mode_result: No help available"""
		param = Conversions.enum_scalar_to_str(trace_mode, enums.TraceModeB)
		response = self._core.io.query_str(f'SENSe:ADEMod:AM:ABSolute:AFSPectrum:RESult? {param}')
		return Conversions.str_to_float(response)
