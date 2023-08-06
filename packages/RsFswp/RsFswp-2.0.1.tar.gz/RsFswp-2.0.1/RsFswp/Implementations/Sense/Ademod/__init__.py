from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ademod:
	"""Ademod commands group definition. 42 total commands, 11 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ademod", core, parent)

	@property
	def af(self):
		"""af commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_af'):
			from .Af import Af
			self._af = Af(self._core, self._cmd_group)
		return self._af

	@property
	def mtime(self):
		"""mtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtime'):
			from .Mtime import Mtime
			self._mtime = Mtime(self._core, self._cmd_group)
		return self._mtime

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Set import Set
			self._set = Set(self._core, self._cmd_group)
		return self._set

	@property
	def am(self):
		"""am commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_am'):
			from .Am import Am
			self._am = Am(self._core, self._cmd_group)
		return self._am

	@property
	def fm(self):
		"""fm commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_fm'):
			from .Fm import Fm
			self._fm = Fm(self._core, self._cmd_group)
		return self._fm

	@property
	def pm(self):
		"""pm commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pm'):
			from .Pm import Pm
			self._pm = Pm(self._core, self._cmd_group)
		return self._pm

	@property
	def spectrum(self):
		"""spectrum commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._cmd_group)
		return self._spectrum

	@property
	def zoom(self):
		"""zoom commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_zoom'):
			from .Zoom import Zoom
			self._zoom = Zoom(self._core, self._cmd_group)
		return self._zoom

	@property
	def squelch(self):
		"""squelch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_squelch'):
			from .Squelch import Squelch
			self._squelch = Squelch(self._core, self._cmd_group)
		return self._squelch

	@property
	def preset(self):
		"""preset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_preset'):
			from .Preset import Preset
			self._preset = Preset(self._core, self._cmd_group)
		return self._preset

	@property
	def adcPrefilter(self):
		"""adcPrefilter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adcPrefilter'):
			from .AdcPrefilter import AdcPrefilter
			self._adcPrefilter = AdcPrefilter(self._core, self._cmd_group)
		return self._adcPrefilter

	def clone(self) -> 'Ademod':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ademod(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
