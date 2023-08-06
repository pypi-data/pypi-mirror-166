from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("insert", core, parent)

	def set(self, file_path: str, touchStone=repcap.TouchStone.Default) -> None:
		"""SCPI: [SENSe]:CORRection:FRESponse:BASeband:USER:SLISt<sli>:INSert \n
		Snippet: driver.sense.correction.fresponse.baseband.user.slist.insert.set(file_path = '1', touchStone = repcap.TouchStone.Default) \n
		No command help available \n
			:param file_path: No help available
			:param touchStone: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Slist')
		"""
		param = Conversions.value_to_quoted_str(file_path)
		touchStone_cmd_val = self._cmd_group.get_repcap_cmd_value(touchStone, repcap.TouchStone)
		self._core.io.write(f'SENSe:CORRection:FRESponse:BASeband:USER:SLISt{touchStone_cmd_val}:INSert {param}')

	def get(self, touchStone=repcap.TouchStone.Default) -> str:
		"""SCPI: [SENSe]:CORRection:FRESponse:BASeband:USER:SLISt<sli>:INSert \n
		Snippet: value: str = driver.sense.correction.fresponse.baseband.user.slist.insert.get(touchStone = repcap.TouchStone.Default) \n
		No command help available \n
			:param touchStone: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Slist')
			:return: file_path: No help available"""
		touchStone_cmd_val = self._cmd_group.get_repcap_cmd_value(touchStone, repcap.TouchStone)
		response = self._core.io.query_str(f'SENSe:CORRection:FRESponse:BASeband:USER:SLISt{touchStone_cmd_val}:INSert?')
		return trim_str_response(response)
