from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, application_group: str, display_name: str) -> None:
		"""SCPI: SYSTem:PLUGin:APPStarter:SELect \n
		Snippet: driver.system.plugin.appStarter.select.set(application_group = '1', display_name = '1') \n
		No command help available \n
			:param application_group: No help available
			:param display_name: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('application_group', application_group, DataType.String), ArgSingle('display_name', display_name, DataType.String))
		self._core.io.write(f'SYSTem:PLUGin:APPStarter:SELect {param}'.rstrip())
