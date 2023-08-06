from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandwidth", core, parent)

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import Mode
			self._mode = Mode(self._core, self._cmd_group)
		return self._mode

	def set(self, bandwidth: float) -> None:
		"""SCPI: [SENSe]:ROSCillator:COUPling:BANDwidth \n
		Snippet: driver.sense.roscillator.coupling.bandwidth.set(bandwidth = 1.0) \n
		This command defines coupling bandwidth for the internal reference frequency.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Options R&S FSWP-B60 or -B61 must be available.
			- Select manual bandwidth mode ([SENSe:]ROSCillator:COUPling:BANDwidth:MODE)  \n
			:param bandwidth: numeric value Bandwidths 20 mHz, 1 Hz and 100 kHz are supported. Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(bandwidth)
		self._core.io.write(f'SENSe:ROSCillator:COUPling:BANDwidth {param}')

	def get(self) -> float:
		"""SCPI: [SENSe]:ROSCillator:COUPling:BANDwidth \n
		Snippet: value: float = driver.sense.roscillator.coupling.bandwidth.get() \n
		This command defines coupling bandwidth for the internal reference frequency.
			INTRO_CMD_HELP: Prerequisites for this command \n
			- Options R&S FSWP-B60 or -B61 must be available.
			- Select manual bandwidth mode ([SENSe:]ROSCillator:COUPling:BANDwidth:MODE)  \n
			:return: bandwidth: numeric value Bandwidths 20 mHz, 1 Hz and 100 kHz are supported. Unit: Hz"""
		response = self._core.io.query_str(f'SENSe:ROSCillator:COUPling:BANDwidth?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Bandwidth':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bandwidth(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
