__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

from datetime import datetime
from pathlib import Path
<<<<<<< HEAD
from typing import Dict
=======
from typing import Dict, Type, Union
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

import requests
from bs4 import BeautifulSoup

from ffmwr.features.base.feature import BaseFeature
from ffmwr.utilities.constants import nfl_team_abbreviation_conversions, nfl_team_abbreviations
from ffmwr.utilities.logger import get_logger
from ffmwr.utilities.settings import AppSettings, get_app_settings_from_env_file
<<<<<<< HEAD
from ffmwr.utilities.utils import generate_normalized_player_key
=======
from ffmwr.utilities.utils import normalize_player_name
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

logger = get_logger(__name__, propagate=False)


class HighRollerFeature(BaseFeature):
    def __init__(
        self,
        season: int,
        week_for_report: int,
        data_dir: Path,
        refresh: bool = False,
        save_data: bool = False,
        offline: bool = False,
    ):
        """Initialize class, load data from Spotrac.com."""
        self.season: int = season

<<<<<<< HEAD
        defense = {
            "CB": "D",
            "DE": "D",
            "DT": "D",
            "FS": "D",
            "ILB": "D",
            "LB": "D",
            "OLB": "D",
            "S": "D",
            "SS": "D",
        }
        offense = {
            "FB": "O",
            "QB": "O",
            "RB": "O",
            "TE": "O",
            "WR": "O",
        }
        special_teams = {
            "K": "S",
            "P": "S",
        }
        offensive_line = {
            "C": "L",
            "G": "L",
            "LS": "L",
            "LT": "L",
            "RT": "L",
        }
        team_defense = {
            "D/ST": "D",
        }
        # position type reference
        self.position_types: Dict[str, str] = {
            **defense,
            **offense,
            **special_teams,
            **offensive_line,
            **team_defense,
        }
=======
        defense = {"CB": "D", "DE": "D", "DT": "D", "FS": "D", "ILB": "D", "LB": "D", "OLB": "D", "S": "D", "SS": "D"}
        offense = {"FB": "O", "QB": "O", "RB": "O", "TE": "O", "WR": "O"}
        special_teams = {"K": "S", "P": "S"}
        offensive_line = {"C": "L", "G": "L", "LS": "L", "LT": "L", "RT": "L"}
        team_defense = {"D/ST": "D"}
        # position type reference
        self.position_types: Dict[str, str] = {**defense, **offense, **special_teams, **offensive_line, **team_defense}
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

        super().__init__(
            "high_roller",
            f"https://www.spotrac.com/nfl/fines/_/year/{self.season}",
            week_for_report,
            data_dir,
<<<<<<< HEAD
            True,  # TODO: decide if team D/ST roll-ups should be included in high roller total
=======
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
            refresh,
            save_data,
            offline,
        )

<<<<<<< HEAD
    # noinspection PyCallingNonCallable
=======
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
    def _get_feature_data(self):
        for team in nfl_team_abbreviations:
            self.feature_data[team] = {
                "position": "D/ST",
                "players": {},
                "violators": [],
<<<<<<< HEAD
                "violators_count": 0,
=======
                "num_violators": 0,
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
                "fines_count": 0,
                "fines_total": 0.0,
                "worst_violation": None,
                "worst_violation_fine": 0.0,
            }

        user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/13.0.2 Safari/605.1.15"
        )
        headers = {"user-agent": user_agent}

        response = requests.get(self.feature_web_base_url, headers=headers)

        html_soup = BeautifulSoup(response.text, "html.parser")
        logger.debug(f"Response URL: {response.url}")
<<<<<<< HEAD
        logger.debug(f"Response (HTML):\n{html_soup.prettify()}")
=======
        logger.debug(f"Response (HTML): {html_soup}")
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

        fined_players = html_soup.find("tbody").find_all("tr", {"class": ""})

        for player in fined_players:
<<<<<<< HEAD
            player_full_name = player.find("a", {"class": "link"}).getText().strip()
            player_team_abbr = player.find("img", {"class": "me-2"}).getText().strip()
            player_position = player.find("td", {"class": "text-left details-sm"}).getText().strip()
            player_position_type = self.position_types[player_position]

            if not player_team_abbr:
                # attempt to retrieve team abbreviation from parent element if img element is missing closing tag
                player_team_abbr = player.find("td", {"class": "text-left details"}).getText().strip()

            # replace player team abbreviation with universal team abbreviation as needed
            if player_team_abbr not in nfl_team_abbreviations:
                if player_team_abbr in nfl_team_abbreviation_conversions.keys():
                    player_team_abbr = nfl_team_abbreviation_conversions[player_team_abbr]
=======
            player_name = player.find("a", {"class": "link"}).getText().strip()
            player_team = player.find("img", {"class": "me-2"}).getText().strip()
            if not player_team:
                # attempt to retrieve team from parent element if img element is missing closing tag
                player_team = player.find("td", {"class": "text-left details"}).getText().strip()

            # TODO: move this cleaning to base feature.py
            # replace player team abbreviation with universal team abbreviation as needed
            if player_team not in nfl_team_abbreviations:
                player_team = nfl_team_abbreviation_conversions[player_team]
            player_position = player.find("td", {"class": "text-left details-sm"}).getText().strip()
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

            try:
                player_violation = player.find("span", {"class": "text-muted"}).getText()[2:].strip()
            except AttributeError as e:
<<<<<<< HEAD
                logger.debug(f"Unable to parse violation for {player_full_name} with error: {repr(e)}")
=======
                logger.debug(f"Unable to parse violation for {player_name} with error: {repr(e)}")
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
                player_violation = None

            player_fine_info = {
                "violation": player_violation,
                "violation_fine": int(
                    "".join(
                        [
                            ch
                            for ch in player.find("td", {"class": "text-center details highlight"}).getText().strip()
                            if ch.isdigit()
                        ]
                    )
                ),
                "violation_season": self.season,
                "violation_date": datetime.strptime(
                    player.find("td", {"class": "text-right details"}).getText().strip(), "%m/%d/%y"
                ).isoformat(),
            }

<<<<<<< HEAD
            normalized_player_key = generate_normalized_player_key(player_full_name, player_team_abbr)

            # add raw player data json to raw_player_data for reference
            self.raw_feature_data[normalized_player_key] = player.prettify()

            if normalized_player_key not in self.feature_data.keys():
                self.feature_data[normalized_player_key] = {
                    **self._get_feature_data_template(
                        player_full_name, player_team_abbr, player_position, player_position_type
                    ),
=======
            if player_name not in self.feature_data.keys():
                self.feature_data[player_name] = {
                    "normalized_name": normalize_player_name(player_name),
                    "team": player_team,
                    "position": player_position,
                    "position_type": self.position_types[player_position],
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
                    "fines": [player_fine_info],
                    "fines_count": 1,
                    "fines_total": player_fine_info["violation_fine"],
                    "worst_violation": player_fine_info["violation"],
                    "worst_violation_fine": player_fine_info["violation_fine"],
                }
            else:
<<<<<<< HEAD
                self.feature_data[normalized_player_key]["fines"].append(player_fine_info)
                self.feature_data[normalized_player_key]["fines"].sort(
                    key=lambda x: (-x["violation_fine"], -datetime.fromisoformat(x["violation_date"]).timestamp())
                )
                self.feature_data[normalized_player_key]["fines_count"] += 1
                self.feature_data[normalized_player_key]["fines_total"] += player_fine_info["violation_fine"]

                worst_violation = self.feature_data[normalized_player_key]["fines"][0]
                self.feature_data[normalized_player_key]["worst_violation"] = worst_violation["violation"]
                self.feature_data[normalized_player_key]["worst_violation_fine"] = worst_violation["violation_fine"]

        for player_key in self.feature_data.keys():
            if self.feature_data[player_key]["position"] != "D/ST":
                player_team_abbr = self.feature_data[player_key]["team_abbr"]

                if player_key not in self.feature_data[player_team_abbr]["players"]:
                    player = self.feature_data[player_key]
                    self.feature_data[player_team_abbr]["players"][player_key] = player
                    self.feature_data[player_team_abbr]["violators"].append(player["full_name"])
                    self.feature_data[player_team_abbr]["violators"] = list(
                        set(self.feature_data[player_team_abbr]["violators"])
                    )
                    self.feature_data[player_team_abbr]["violators_count"] = len(
                        self.feature_data[player_team_abbr]["violators"]
                    )
                    self.feature_data[player_team_abbr]["fines_count"] += player["fines_count"]
                    self.feature_data[player_team_abbr]["fines_total"] += player["fines_total"]
                    if player["worst_violation_fine"] >= self.feature_data[player_team_abbr]["worst_violation_fine"]:
                        self.feature_data[player_team_abbr]["worst_violation"] = player["worst_violation"]
                        self.feature_data[player_team_abbr]["worst_violation_fine"] = player["worst_violation_fine"]

    def get_player_worst_violation(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> str:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "worst_violation", str
        )

    def get_player_worst_violation_fine(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> float:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "worst_violation_fine", float
        )

    def get_player_fines_total(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> float:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "fines_total", float
        )

    def get_player_num_violators(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> int:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "violators_count", int
=======
                self.feature_data[player_name]["fines"].append(player_fine_info)
                self.feature_data[player_name]["fines"].sort(
                    key=lambda x: (-x["violation_fine"], -datetime.fromisoformat(x["violation_date"]).timestamp())
                )
                self.feature_data[player_name]["fines_count"] += 1
                self.feature_data[player_name]["fines_total"] += player_fine_info["violation_fine"]

                worst_violation = self.feature_data[player_name]["fines"][0]
                self.feature_data[player_name]["worst_violation"] = worst_violation["violation"]
                self.feature_data[player_name]["worst_violation_fine"] = worst_violation["violation_fine"]

        for player_name in self.feature_data.keys():
            if self.feature_data[player_name]["position"] != "D/ST":
                player_team = self.feature_data[player_name]["team"]

                if player_name not in self.feature_data[player_team]["players"]:
                    player = self.feature_data[player_name]
                    self.feature_data[player_team]["players"][player_name] = player
                    self.feature_data[player_team]["violators"].append(player_name)
                    self.feature_data[player_team]["violators"] = list(set(self.feature_data[player_team]["violators"]))
                    self.feature_data[player_team]["num_violators"] = len(self.feature_data[player_team]["violators"])
                    self.feature_data[player_team]["fines_count"] += player["fines_count"]
                    self.feature_data[player_team]["fines_total"] += player["fines_total"]
                    if player["worst_violation_fine"] >= self.feature_data[player_team]["worst_violation_fine"]:
                        self.feature_data[player_team]["worst_violation"] = player["worst_violation"]
                        self.feature_data[player_team]["worst_violation_fine"] = player["worst_violation_fine"]

    def _get_player_high_roller_stats(
        self,
        player_first_name: str,
        player_last_name: str,
        player_team_abbr: str,
        player_pos: str,
        key_str: str,
        key_type: Type,
    ) -> Union[str, float, int]:
        player_full_name = (
            f"{player_first_name.title() if player_first_name else ''}"
            f"{' ' if player_first_name and player_last_name else ''}"
            f"{player_last_name.title() if player_last_name else ''}"
        ).strip()

        if player_full_name in self.feature_data.keys():
            return self.feature_data[player_full_name].get(key_str, key_type())
        else:
            logger.debug(
                f'No {self.feature_type_title} data found for player "{player_full_name}". '
                f"Run report with the -r flag (--refresh-web-data) to refresh all external web data and try again."
            )

            player = {
                "position": player_pos,
                "fines_count": 0,
                "fines_total": 0.0,
                "worst_violation": None,
                "worst_violation_fine": 0.0,
            }
            if player_pos == "D/ST":
                player.update(
                    {
                        "players": {},
                        "violators": [],
                        "num_violators": 0,
                    }
                )
            else:
                player.update(
                    {
                        "normalized_name": normalize_player_name(player_full_name),
                        "team": player_team_abbr,
                        "fines": [],
                    }
                )

            self.feature_data[player_full_name] = player

            return self.feature_data[player_full_name][key_str]

    def get_player_worst_violation(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> str:
        return self._get_player_high_roller_stats(
            player_first_name, player_last_name, player_team, player_pos, "worst_violation", str
        )

    def get_player_worst_violation_fine(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> float:
        return self._get_player_high_roller_stats(
            player_first_name, player_last_name, player_team, player_pos, "worst_violation_fine", float
        )

    def get_player_fines_total(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> float:
        return self._get_player_high_roller_stats(
            player_first_name, player_last_name, player_team, player_pos, "fines_total", float
        )

    def get_player_num_violators(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> int:
        return self._get_player_high_roller_stats(
            player_first_name, player_last_name, player_team, player_pos, "num_violators", int
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
        )


if __name__ == "__main__":
    local_root_directory = Path(__file__).parent.parent.parent

    local_settings: AppSettings = get_app_settings_from_env_file(local_root_directory / ".env")

    local_high_roller_feature = HighRollerFeature(
        local_settings.season,
        1,
        local_root_directory / local_settings.data_dir_path / "tests" / "feature_data",
        refresh=True,
        save_data=True,
        offline=False,
    )
