from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srange:
	"""Srange commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("srange", core, parent)

	def set(self, search_range: enums.SearchRange) -> None:
		"""SCPI: [SENSe]:CREFerence:SRANge \n
		Snippet: driver.applications.k50Spurious.sense.creference.srange.set(search_range = enums.SearchRange.GMAXimum) \n
		Determines the search area for the automatic carrier measurement function. \n
			:param search_range: GMAXimum | RMAXimum GMAXimum Global maximum: The maximum peak in the entire measurement span is determined. RMAXimum Range maximum: The maximum peak is searched only in the specified range.
		"""
		param = Conversions.enum_scalar_to_str(search_range, enums.SearchRange)
		self._core.io.write(f'SENSe:CREFerence:SRANge {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.SearchRange:
		"""SCPI: [SENSe]:CREFerence:SRANge \n
		Snippet: value: enums.SearchRange = driver.applications.k50Spurious.sense.creference.srange.get() \n
		Determines the search area for the automatic carrier measurement function. \n
			:return: search_range: GMAXimum | RMAXimum GMAXimum Global maximum: The maximum peak in the entire measurement span is determined. RMAXimum Range maximum: The maximum peak is searched only in the specified range."""
		response = self._core.io.query_str(f'SENSe:CREFerence:SRANge?')
		return Conversions.str_to_scalar_enum(response, enums.SearchRange)
