from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeviceFootprint:
	"""DeviceFootprint commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("deviceFootprint", core, parent)

	def get(self) -> str:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: value: str = driver.system.deviceFootprint.get() \n
		No command help available \n
			:return: xxx: No help available"""
		response = self._core.io.query_str(f'SYSTem:DFPRint?')
		return trim_str_response(response)
