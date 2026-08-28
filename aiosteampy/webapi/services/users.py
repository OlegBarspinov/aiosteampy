"""Client for interacting with `ISteamUser`."""

from collections.abc import Sequence

from ...id import SteamID
from ._base import JsonResponse, SteamWebApiServiceBase

MAX_SUMMARIES_STEAMIDS = 100  # current effective limit for one request


class UsersServiceClient(SteamWebApiServiceBase):
    """Users service client."""

    __slots__ = ()

    SERVICE_NAME = "ISteamUser"

    def get_player_summaries(
        self,
        steamids: str | SteamID | Sequence[str | SteamID],
    ) -> JsonResponse:
        """
        Get public profile data for given users.
        Profile avatars and names are returned regardless of profile privacy settings.

        :param steamids: one or more (up to 100) 64-bit SteamIDs.
        :return: response mapping with `response.players` list of profile summaries.
        """
        if isinstance(steamids, (str, SteamID)):
            steamids = (steamids,)
        steamids = tuple(steamids)
        if not 0 < len(steamids) <= MAX_SUMMARIES_STEAMIDS:
            raise ValueError(f"Amount of `steamids` must be between 1 and {MAX_SUMMARIES_STEAMIDS}")

        params = {"steamids": ",".join(str(sid) for sid in steamids)}
        return self._urlencoded("GetPlayerSummaries", version=2, params=params, auth=True)
