from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Next:
	"""Next commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("next", core, parent)

	def set(self) -> None:
		"""SCPI: MMEMory:STORe:STATe:NEXT \n
		Snippet: driver.massMemory.store.state.next.set() \n
		This command saves the current instrument configuration in a *.dfl file. The file name depends on the one you have set
		with method RsFswp.MassMemory.Store.State.set. This command adds a consecutive number to the file name. \n
		"""
		self._core.io.write(f'MMEMory:STORe:STATe:NEXT')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: MMEMory:STORe:STATe:NEXT \n
		Snippet: driver.massMemory.store.state.next.set_with_opc() \n
		This command saves the current instrument configuration in a *.dfl file. The file name depends on the one you have set
		with method RsFswp.MassMemory.Store.State.set. This command adds a consecutive number to the file name. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsFswp.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'MMEMory:STORe:STATe:NEXT', opc_timeout_ms)
