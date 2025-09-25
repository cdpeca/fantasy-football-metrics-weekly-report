__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"

import itertools
import json
import re
from collections import OrderedDict
from pathlib import Path
<<<<<<< HEAD
from typing import Dict

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout

from ffmwr.features.base.feature import BaseFeature
from ffmwr.utilities.constants import nfl_team_abbreviations
from ffmwr.utilities.logger import get_logger
from ffmwr.utilities.settings import AppSettings, get_app_settings_from_env_file
from ffmwr.utilities.utils import generate_normalized_player_key
=======
from string import capwords
from typing import Any, Dict, Optional, Union

import requests
from bs4 import BeautifulSoup

from ffmwr.features.base.feature import BaseFeature
from ffmwr.utilities.constants import nfl_team_abbreviation_conversions, nfl_team_abbreviations
from ffmwr.utilities.logger import get_logger
from ffmwr.utilities.settings import AppSettings, get_app_settings_from_env_file
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

logger = get_logger(__name__, propagate=False)


class BadBoyFeature(BaseFeature):
    def __init__(
        self,
        week_for_report: int,
        root_dir: Path,
        data_dir: Path,
        refresh: bool = False,
        save_data: bool = False,
        offline: bool = False,
    ):
        """Initialize class, load data from USA Today NFL Arrest DB. Combine defensive player data"""

        defense = {
            "C": "D",
            "CB": "D",
            "DB": "D",
            "DE": "D",
            "DE/DT": "D",
            "DT": "D",
            "LB": "D",
            "S": "D",
            "Safety": "D",
        }
<<<<<<< HEAD
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
            "OG": "L",
            "OL": "L",
            "OT": "L",
        }
        coaching_staff = {
            "OC": "C",
        }
=======
        offense = {"FB": "O", "QB": "O", "RB": "O", "TE": "O", "WR": "O"}
        special_teams = {"K": "S", "P": "S"}
        offensive_line = {"OG": "L", "OL": "L", "OT": "L"}
        coaching_staff = {"OC": "C"}
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
        # position type reference
        self.position_types: Dict[str, str] = {
            **defense,
            **offense,
            **special_teams,
            **offensive_line,
            **coaching_staff,
        }

        self.resource_files_dir = root_dir / "resources" / "files"

        # Load the scoring based on crime categories
        with open(self.resource_files_dir / "crime_categories.json", mode="r", encoding="utf-8") as crimes:
            self.crime_rankings = json.load(crimes)
            logger.debug("Crime categories loaded.")

        # for outputting all unique crime categories found in the USA Today NFL arrests data
        self.unique_crime_categories_for_output = {}

        super().__init__(
            "bad_boy",
            "https://www.usatoday.com/sports/nfl/arrests",
            week_for_report,
            data_dir,
<<<<<<< HEAD
<<<<<<< HEAD
            True,  # TODO: figure out how to include only ACTIVE players in team D/ST roll-ups
=======
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
=======
            True,  # TODO: figure out how to include only ACTIVE players in team D/ST roll-ups
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)
            refresh,
            save_data,
            offline,
        )

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)
    def _get_ajax_nonce(self):
        logger.debug(f"Retrieving AJAX nonce for {self.feature_type_title} feature.")

        res = requests.get(self.feature_web_base_url)
        soup = BeautifulSoup(res.text, "html.parser")
        cdata = re.search("var sitedata = (.*);", soup.find(string=re.compile("CDATA"))).group(1)
        return json.loads(cdata)["ajax_nonce"]

<<<<<<< HEAD
=======
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
=======
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)
    # noinspection DuplicatedCode
    def _get_feature_data(self) -> None:
        logger.debug("Retrieving bad boy feature data from the web.")

<<<<<<< HEAD
<<<<<<< HEAD
        ajax_nonce = self._get_ajax_nonce()
=======
        res = requests.get(self.feature_web_base_url)
        soup = BeautifulSoup(res.text, "html.parser")
        cdata = re.search("var sitedata = (.*);", soup.find(string=re.compile("CDATA"))).group(1)
        ajax_nonce = json.loads(cdata)["ajax_nonce"]
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
=======
        ajax_nonce = self._get_ajax_nonce()
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)

        usa_today_nfl_arrest_url = "https://databases.usatoday.com/wp-admin/admin-ajax.php"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        """
        Example ajax query body:
        
        example_body = (
            'action=cspFetchTable&'
            'security=61406e4feb&'
            'pageID=10&'
            'sortBy=Date&'
            'sortOrder=desc&'
            'searches={"Last_name":"hill","Team":"SEA","First_name":"leroy"}'
        )
        """
        arrests = []
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)
        for ndx, team in enumerate(nfl_team_abbreviations):
            # the usatoday arrests data uses JAC to abbreviate Jacksonville Jaguars
            if team == "JAX":
                team = "JAC"
<<<<<<< HEAD

            logger.debug(f"Retrieving bad boy feature data for NFL team: {team}.")

            try:
                page_num = 1
                body = (
                    f"action=cspFetchTable"
                    f"&security={ajax_nonce}"
                    f"&pageID=10"
                    f"&sortBy=Date"
                    f"&sortOrder=desc"
                    f"&page={page_num}"
                    f'&searches={{"Team":"{team}"}}'
                )

                res_json = requests.post(usa_today_nfl_arrest_url, data=body, headers=headers).json()

                arrests_data = res_json["data"]["Result"]

                for arrest in arrests_data:
                    arrests.append(
                        {
                            "full_name": f"{arrest['First_name']} {arrest['Last_name']}",
                            "team_abbr": (
                                "FA"
                                if (arrest["Team"] == "Free agent" or arrest["Team"] == "Free Agent")
                                else arrest["Team"]
                            ),
                            "date": arrest["Date"],
                            "position": arrest["Position"],
                            "position_type": self.position_types[arrest["Position"]],
                            "case": arrest["Case_1"].upper(),
                            "crime": arrest["Category"].upper(),
                            "description": arrest["Description"],
                            "outcome": arrest["Outcome"],
                        }
                    )

                total_results = res_json["data"]["totalResults"]

                # the USA Today NFL arrests database only retrieves 20 entries per request
                if total_results > 20:
                    # add extra page to include last page of results if they exist
                    num_pages = (total_results // 20) + (1 if total_results % 20 > 0 else 0)

                    for page in range(2, num_pages + 1):
                        page_num += 1
                        body = (
                            f"action=cspFetchTable"
                            f"&security={ajax_nonce}"
                            f"&pageID=10"
                            f"&sortBy=Date"
                            f"&sortOrder=desc"
                            f"&page={page_num}"
                            f'&searches={{"Team":"{team}"}}'
                        )

                        r = requests.post(usa_today_nfl_arrest_url, data=body, headers=headers)
                        resp_json = r.json()

                        arrests_data = resp_json["data"]["Result"]

                        for arrest in arrests_data:
                            arrests.append(
                                {
                                    "full_name": f"{arrest['First_name']} {arrest['Last_name']}",
                                    "team_abbr": (
                                        "FA"
                                        if (arrest["Team"] == "Free agent" or arrest["Team"] == "Free Agent")
                                        else arrest["Team"]
                                    ),
                                    "date": arrest["Date"],
                                    "position": arrest["Position"],
                                    "position_type": self.position_types[arrest["Position"]],
                                    "case": arrest["Case_1"].upper(),
                                    "crime": arrest["Category"].upper(),
                                    "description": arrest["Description"],
                                    "outcome": arrest["Outcome"],
                                }
                            )

            except ConnectTimeout as e:
                logger.debug(f"Connection timed out for {self.feature_type_title} feature: {e}")
                logger.debug(f"Refreshing AJAX nonce and trying again for NFL team {team}.")
                # refresh the AJAX nonce
                ajax_nonce = self._get_ajax_nonce()
                # insert the team for which the AJAX queries timed out back into the list before the next loop
                nfl_team_abbreviations.insert(ndx + 1, team)

        arrests_by_team = {
            key: list(group)
            for key, group in itertools.groupby(sorted(arrests, key=lambda x: x["team_abbr"]), lambda x: x["team_abbr"])
=======
        for team in nfl_team_abbreviations:
            page_num = 1
            body = (
                f"action=cspFetchTable"
                f"&security={ajax_nonce}"
                f"&pageID=10"
                f"&sortBy=Date"
                f"&sortOrder=desc"
                f"&page={page_num}"
                f'&searches={{"Team":"{team}"}}'
            )
=======
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)

            logger.debug(f"Retrieving bad boy feature data for NFL team: {team}.")

<<<<<<< HEAD
            arrests_data = res_json["data"]["Result"]

            for arrest in arrests_data:
                arrests.append(
                    {
                        "name": f"{arrest['First_name']} {arrest['Last_name']}",
                        "team": (
                            "FA"
                            if (arrest["Team"] == "Free agent" or arrest["Team"] == "Free Agent")
                            else arrest["Team"]
                        ),
                        "date": arrest["Date"],
                        "position": arrest["Position"],
                        "position_type": self.position_types[arrest["Position"]],
                        "case": arrest["Case_1"].upper(),
                        "crime": arrest["Category"].upper(),
                        "description": arrest["Description"],
                        "outcome": arrest["Outcome"],
                    }
=======
            try:
                page_num = 1
                body = (
                    f"action=cspFetchTable"
                    f"&security={ajax_nonce}"
                    f"&pageID=10"
                    f"&sortBy=Date"
                    f"&sortOrder=desc"
                    f"&page={page_num}"
                    f'&searches={{"Team":"{team}"}}'
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)
                )

                res_json = requests.post(usa_today_nfl_arrest_url, data=body, headers=headers).json()

                arrests_data = res_json["data"]["Result"]

                for arrest in arrests_data:
                    arrests.append(
                        {
                            "full_name": f"{arrest['First_name']} {arrest['Last_name']}",
                            "team_abbr": (
                                "FA"
                                if (arrest["Team"] == "Free agent" or arrest["Team"] == "Free Agent")
                                else arrest["Team"]
                            ),
                            "date": arrest["Date"],
                            "position": arrest["Position"],
                            "position_type": self.position_types[arrest["Position"]],
                            "case": arrest["Case_1"].upper(),
                            "crime": arrest["Category"].upper(),
                            "description": arrest["Description"],
                            "outcome": arrest["Outcome"],
                        }
                    )

                total_results = res_json["data"]["totalResults"]

                # the USA Today NFL arrests database only retrieves 20 entries per request
                if total_results > 20:
                    # add extra page to include last page of results if they exist
                    num_pages = (total_results // 20) + (1 if total_results % 20 > 0 else 0)

<<<<<<< HEAD
                    for arrest in arrests_data:
                        arrests.append(
                            {
                                "name": f"{arrest['First_name']} {arrest['Last_name']}",
                                "team": (
                                    "FA"
                                    if (arrest["Team"] == "Free agent" or arrest["Team"] == "Free Agent")
                                    else arrest["Team"]
                                ),
                                "date": arrest["Date"],
                                "position": arrest["Position"],
                                "position_type": self.position_types[arrest["Position"]],
                                "case": arrest["Case_1"].upper(),
                                "crime": arrest["Category"].upper(),
                                "description": arrest["Description"],
                                "outcome": arrest["Outcome"],
                            }
=======
                    for page in range(2, num_pages + 1):
                        page_num += 1
                        body = (
                            f"action=cspFetchTable"
                            f"&security={ajax_nonce}"
                            f"&pageID=10"
                            f"&sortBy=Date"
                            f"&sortOrder=desc"
                            f"&page={page_num}"
                            f'&searches={{"Team":"{team}"}}'
>>>>>>> fc231fd (v21.0.0 change project from requirements.txt to pyproject.toml, fix gitpython bug, fix empty high roller data bug, add pre-deploy script for automated versioning, change github actions image to uv python, change docker image to uv python, and update documentation)
                        )

                        r = requests.post(usa_today_nfl_arrest_url, data=body, headers=headers)
                        resp_json = r.json()

                        arrests_data = resp_json["data"]["Result"]

                        for arrest in arrests_data:
                            arrests.append(
                                {
                                    "full_name": f"{arrest['First_name']} {arrest['Last_name']}",
                                    "team_abbr": (
                                        "FA"
                                        if (arrest["Team"] == "Free agent" or arrest["Team"] == "Free Agent")
                                        else arrest["Team"]
                                    ),
                                    "date": arrest["Date"],
                                    "position": arrest["Position"],
                                    "position_type": self.position_types[arrest["Position"]],
                                    "case": arrest["Case_1"].upper(),
                                    "crime": arrest["Category"].upper(),
                                    "description": arrest["Description"],
                                    "outcome": arrest["Outcome"],
                                }
                            )

            except ConnectTimeout as e:
                logger.debug(f"Connection timed out for {self.feature_type_title} feature: {e}")
                logger.debug(f"Refreshing AJAX nonce and trying again for NFL team {team}.")
                # refresh the AJAX nonce
                ajax_nonce = self._get_ajax_nonce()
                # insert the team for which the AJAX queries timed out back into the list before the next loop
                nfl_team_abbreviations.insert(ndx + 1, team)

        arrests_by_team = {
            key: list(group)
            for key, group in itertools.groupby(sorted(arrests, key=lambda x: x["team"]), lambda x: x["team"])
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
        }

        for team_abbr in nfl_team_abbreviations:
            if team_arrests := arrests_by_team.get(team_abbr):
                nfl_team: Dict = {
<<<<<<< HEAD
                    "position": "D/ST",
                    "players": {},
                    "offenders": [],
                    "offenders_count": 0,
                    "worst_offense": None,
                    "worst_offense_points": 0,
                    "bad_boy_points_total": 0,
                }

                for player_arrest in team_arrests:
                    player_full_name = player_arrest.get("full_name")
                    player_position = player_arrest.get("position")
                    player_position_type = player_arrest.get("position_type")
                    offense_category = str.upper(player_arrest.get("crime"))

                    normalized_player_key = generate_normalized_player_key(player_full_name, team_abbr)

=======
                    "pos": "D/ST",
                    "players": {},
                    "total_points": 0,
                    "offenders": [],
                    "num_offenders": 0,
                    "worst_offense": None,
                    "worst_offense_points": 0,
                }

                for player_arrest in team_arrests:
                    player_name = player_arrest.get("name")
                    player_pos = player_arrest.get("position")
                    player_pos_type = player_arrest.get("position_type")
                    offense_category = str.upper(player_arrest.get("crime"))

>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
                    # Add each crime to output categories for generation of crime_categories.new.json file, which can
                    # be used to replace the existing crime_categories.json file. Each new crime categories will default
                    # to a score of 0, and must have its score manually assigned within the json file.
                    self.unique_crime_categories_for_output[offense_category] = self.crime_rankings.get(
                        offense_category, 0
                    )

<<<<<<< HEAD
                    # add raw player data json to raw_player_data for reference
                    self.raw_feature_data[normalized_player_key] = player_arrest
=======
                    # add raw player arrest data to raw data collection
                    self.raw_feature_data[player_name] = player_arrest
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

                    if offense_category in self.crime_rankings.keys():
                        offense_points = self.crime_rankings.get(offense_category)
                    else:
                        offense_points = 0
                        logger.warning(f'Crime ranking not found: "{offense_category}". Assigning score of 0.')

                    nfl_player = {
<<<<<<< HEAD
                        **self._get_feature_data_template(
                            player_full_name, team_abbr, player_position, self.position_types[player_position]
                        ),
                        "offenses": [],
                        "worst_offense": None,
                        "worst_offense_points": 0,
                        "bad_boy_points_total": 0,
=======
                        "team": team_abbr,
                        "pos": player_pos,
                        "offenses": [],
                        "total_points": 0,
                        "worst_offense": None,
                        "worst_offense_points": 0,
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
                    }

                    # update player entry
                    nfl_player["offenses"].append({offense_category: offense_points})
<<<<<<< HEAD
                    nfl_player["bad_boy_points_total"] += offense_points

                    if offense_points > nfl_player["worst_offense_points"]:
                        # noinspection PyTypeChecker
                        nfl_player["worst_offense"] = offense_category
                        nfl_player["worst_offense_points"] = offense_points

                    self.feature_data[normalized_player_key] = nfl_player

                    # update team DEF entry
                    if player_position_type == "D":
                        nfl_team["players"][normalized_player_key] = self.feature_data[normalized_player_key]
                        nfl_team["bad_boy_points_total"] += offense_points
                        nfl_team["offenders"].append(player_full_name)
                        nfl_team["offenders"] = list(set(nfl_team["offenders"]))
                        nfl_team["offenders_count"] = len(nfl_team["offenders"])
=======
                    nfl_player["total_points"] += offense_points

                    if offense_points > nfl_player["worst_offense_points"]:
                        nfl_player["worst_offense"] = offense_category
                        nfl_player["worst_offense_points"] = offense_points

                    self.feature_data[player_name] = nfl_player

                    # update team DEF entry
                    if player_pos_type == "D":
                        nfl_team["players"][player_name] = self.feature_data[player_name]
                        nfl_team["total_points"] += offense_points
                        nfl_team["offenders"].append(player_name)
                        nfl_team["offenders"] = list(set(nfl_team["offenders"]))
                        nfl_team["num_offenders"] = len(nfl_team["offenders"])
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

                        if offense_points > nfl_team["worst_offense_points"]:
                            nfl_team["worst_offense"] = offense_category
                            nfl_team["worst_offense_points"] = offense_points

                self.feature_data[team_abbr] = nfl_team

<<<<<<< HEAD
    def get_player_bad_boy_crime(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> str:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "worst_offense", str
        )

    def get_player_bad_boy_points(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> int:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "bad_boy_points_total", int
        )

    def get_player_bad_boy_num_offenders(
        self, player_first_name: str, player_last_name: str, player_team_abbr: str, player_position: str
    ) -> int:
        return self._get_player_feature_stats(
            player_first_name, player_last_name, player_team_abbr, player_position, "offenders_count", int
        )
=======
    def _get_player_bad_boy_stats(
        self,
        player_first_name: str,
        player_last_name: str,
        player_team_abbr: str,
        player_pos: str,
        key_str: Optional[str] = None,
    ) -> Union[int, str, Dict[str, Any]]:
        """Looks up given player and returns number of "bad boy" points based on custom crime scoring.

        TODO: maybe limit for years and adjust defensive players rolling up to DEF team as it skews DEF scores high
        :param player_first_name: First name of player to look up
        :param player_last_name: Last name of player to look up
        :param player_team_abbr: Player's team (maybe limit to only crimes while on that team...or for DEF players???)
        :param player_pos: Player's position
        :param key_str: which player information to retrieve (crime: "worst_offense" or bad boy points: "total_points")
        :return: Ether integer number of bad boy points or crime recorded (depending on key_str)
        """
        player_team = str.upper(player_team_abbr) if player_team_abbr else "?"
        if player_team not in nfl_team_abbreviations:
            if player_team in nfl_team_abbreviation_conversions.keys():
                player_team = nfl_team_abbreviation_conversions[player_team]

        player_full_name = (
            f"{capwords(player_first_name) if player_first_name else ''}"
            f"{' ' if player_first_name and player_last_name else ''}"
            f"{capwords(player_last_name) if player_last_name else ''}"
        ).strip()

        # TODO: figure out how to include only ACTIVE players in team DEF roll-ups
        if player_pos == "D/ST":
            # player_full_name = player_team
            player_full_name = "TEMPORARY DISABLING OF TEAM DEFENSES IN BAD BOY POINTS"
        if player_full_name in self.feature_data:
            return self.feature_data[player_full_name][key_str] if key_str else self.feature_data[player_full_name]
        else:
            logger.debug(
                f"Player not found: {player_full_name}. Setting crime category and bad boy points to 0. Run report "
                f"with the -r flag (--refresh-web-data) to refresh all external web data and try again."
            )

            self.feature_data[player_full_name] = {
                "team": player_team,
                "pos": player_pos,
                "offenses": [],
                "total_points": 0,
                "worst_offense": None,
                "worst_offense_points": 0,
            }
            return self.feature_data[player_full_name][key_str] if key_str else self.feature_data[player_full_name]

    def get_player_bad_boy_crime(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> str:
        return self._get_player_bad_boy_stats(
            player_first_name, player_last_name, player_team, player_pos, "worst_offense"
        )

    def get_player_bad_boy_points(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> int:
        return self._get_player_bad_boy_stats(
            player_first_name, player_last_name, player_team, player_pos, "total_points"
        )

    def get_player_bad_boy_num_offenders(
        self, player_first_name: str, player_last_name: str, player_team: str, player_pos: str
    ) -> int:
        player_bad_boy_stats = self._get_player_bad_boy_stats(
            player_first_name, player_last_name, player_team, player_pos
        )
        if player_bad_boy_stats.get("pos") == "D/ST":
            return player_bad_boy_stats.get("num_offenders")
        else:
            return 0
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)

    def generate_crime_categories_json(self):
        unique_crimes = OrderedDict(sorted(self.unique_crime_categories_for_output.items(), key=lambda k_v: k_v[0]))
        with open(self.resource_files_dir / "crime_categories.new.json", mode="w", encoding="utf-8") as crimes:
<<<<<<< HEAD
            # noinspection PyTypeChecker
=======
>>>>>>> 7d5cbd8 (refactored entire codebase into sudirectory, linted using ruff and bandit, improved logging, cleaned up some runtime business logic)
            json.dump(unique_crimes, crimes, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    local_root_directory = Path(__file__).parent.parent.parent

    local_settings: AppSettings = get_app_settings_from_env_file(local_root_directory / ".env")

    local_bad_boy_feature = BadBoyFeature(
        1,
        local_root_directory,
        local_root_directory / local_settings.data_dir_path / "tests" / "feature_data",
        refresh=True,
        save_data=True,
        offline=False,
    )
