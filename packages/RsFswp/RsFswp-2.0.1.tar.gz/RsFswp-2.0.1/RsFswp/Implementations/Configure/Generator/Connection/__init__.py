from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Connection:
	"""Connection commands group definition. 2 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	@property
	def cstate(self):
		"""cstate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cstate'):
			from .Cstate import Cstate
			self._cstate = Cstate(self._core, self._cmd_group)
		return self._cstate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	def clone(self) -> 'Connection':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Connection(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
