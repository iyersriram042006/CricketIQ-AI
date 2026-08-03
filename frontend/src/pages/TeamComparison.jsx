import { useState } from "react";

import api from "../services/api";
import TeamSearch from "../components/TeamSearch";
import TEAM_LOGOS from "../utils/teamLogos";

function TeamComparison() {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [result, setResult] = useState(null);

  const compareTeams = () => {
    if (!team1 || !team2) return;

    api
      .get("/teams/compare", {
        params: {
          team1,
          team2,
        },
      })
      .then((res) => {
        setResult(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Team Comparison
      </h1>

      <div className="mb-8 grid gap-4 md:grid-cols-3">

        <TeamSearch
          onSelect={setTeam1}
        />

        <TeamSearch
          onSelect={setTeam2}
        />

        <button
          onClick={compareTeams}
          disabled={!team1 || !team2}
          className="rounded-lg bg-blue-600 px-6 py-3 hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-600"
        >
          Compare
        </button>

      </div>

      {result && (

        <div className="rounded-xl bg-slate-800 p-8">

          <div className="mb-10 flex items-center justify-center gap-12">

            <div className="flex flex-col items-center">

              <img
                src={TEAM_LOGOS[team1]}
                alt={team1}
                className="mb-3 h-20 w-20 object-contain"
              />

              <p className="text-center text-lg font-semibold">
                {team1}
              </p>

            </div>

            <div className="text-4xl font-bold text-slate-400">
              VS
            </div>

            <div className="flex flex-col items-center">

              <img
                src={TEAM_LOGOS[team2]}
                alt={team2}
                className="mb-3 h-20 w-20 object-contain"
              />

              <p className="text-center text-lg font-semibold">
                {team2}
              </p>

            </div>

          </div>

          <h2 className="mb-6 text-center text-3xl font-bold">
            Head to Head
          </h2>

          <div className="grid gap-6 md:grid-cols-3">

            <div className="rounded-lg bg-slate-700 p-6">

              <p className="text-slate-300">
                Matches Played
              </p>

              <p className="text-4xl font-bold">
                {result.matches}
              </p>

            </div>

            <div className="rounded-lg bg-slate-700 p-6">

              <p className="text-slate-300">
                {team1} Wins
              </p>

              <p className="text-4xl font-bold">
                {result.team1_wins}
              </p>

            </div>

            <div className="rounded-lg bg-slate-700 p-6">

              <p className="text-slate-300">
                {team2} Wins
              </p>

              <p className="text-4xl font-bold">
                {result.team2_wins}
              </p>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default TeamComparison;