from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 10 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import All
			self._all = All(self._core, self._cmd_group)
		return self._all

	@property
	def achannel(self):
		"""achannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_achannel'):
			from .Achannel import Achannel
			self._achannel = Achannel(self._core, self._cmd_group)
		return self._achannel

	@property
	def uaChannel(self):
		"""uaChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uaChannel'):
			from .UaChannel import UaChannel
			self._uaChannel = UaChannel(self._core, self._cmd_group)
		return self._uaChannel

	@property
	def alternate(self):
		"""alternate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alternate'):
			from .Alternate import Alternate
			self._alternate = Alternate(self._core, self._cmd_group)
		return self._alternate

	@property
	def ualternate(self):
		"""ualternate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ualternate'):
			from .Ualternate import Ualternate
			self._ualternate = Ualternate(self._core, self._cmd_group)
		return self._ualternate

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Channel import Channel
			self._channel = Channel(self._core, self._cmd_group)
		return self._channel

	@property
	def sblock(self):
		"""sblock commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sblock'):
			from .Sblock import Sblock
			self._sblock = Sblock(self._core, self._cmd_group)
		return self._sblock

	@property
	def gap(self):
		"""gap commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gap'):
			from .Gap import Gap
			self._gap = Gap(self._core, self._cmd_group)
		return self._gap

	def clone(self) -> 'State':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = State(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
