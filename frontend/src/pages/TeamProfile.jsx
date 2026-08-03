import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TEAM_LOGOS from "../utils/teamLogos";
import api from "../services/api";

function TeamProfile() {
  const { teamName } = useParams();

  const [team, setTeam] = useState(null);
  const [topBatters, setTopBatters] = useState([]);
  const [topBowlers, setTopBowlers] = useState([]);
  const [recentForm, setRecentForm] = useState([]);

  useEffect(() => {
    api
      .get(`/teams/${teamName}`)
      .then((res) => {
        setTeam(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/teams/${teamName}/stats`)
      .then((res) => {
        setTopBatters(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/teams/${teamName}/bowlers`)
      .then((res) => {
        setTopBowlers(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/teams/${teamName}/recent-form`)
      .then((res) => {
        setRecentForm(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

  }, [teamName]);

  if (!team) {
    return (
      <div className="text-2xl text-white">
        Loading...
      </div>
    );
  }

  const losses = team.matches - team.wins;

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Team Profile
      </h1>

      <div className="rounded-xl bg-slate-800 p-8">

        <div className="mb-6 flex items-center gap-4">

        <img
          src={TEAM_LOGOS[team.team_name]}
          alt={team.team_name}
          className="h-16 w-16 object-contain"
        />

        <h2 className="text-3xl font-semibold">
          {team.team_name}
        </h2>

      </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Matches
            </p>

            <p className="text-3xl font-bold">
              {team.matches}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Wins
            </p>

            <p className="text-3xl font-bold">
              {team.wins}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Losses
            </p>

            <p className="text-3xl font-bold">
              {losses}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Win %
            </p>

            <p className="text-3xl font-bold">
              {team.win_percentage}%
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Highest Score
            </p>

            <p className="text-3xl font-bold">
              {team.highest_score}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Lowest Score
            </p>

            <p className="text-3xl font-bold">
              {team.lowest_score}
            </p>
          </div>

        </div>

        <div className="mt-10">

          <h3 className="mb-5 text-2xl font-bold">
            Recent Form
          </h3>

          <div className="flex gap-3">

            {recentForm.map((match, index) => (

              <div
                key={index}
                className={`flex h-12 w-12 items-center justify-center rounded-full text-lg font-bold text-white ${
                  match.result === "W"
                    ? "bg-green-600"
                    : "bg-red-600"
                }`}
              >
                {match.result}
              </div>

            ))}

          </div>

        </div>

        <div className="mt-10">

          <h3 className="mb-5 text-2xl font-bold">
            Top Run Scorers
          </h3>

          <table className="w-full">

            <thead>

              <tr className="border-b border-slate-700">
                <th className="py-3 text-left">
                  Player
                </th>

                <th className="text-right">
                  Runs
                </th>
              </tr>

            </thead>

            <tbody>

              {topBatters.map((player) => (

                <tr
                  key={player.batter}
                  className="border-b border-slate-700"
                >

                  <td className="py-3">
                    {player.batter}
                  </td>

                  <td className="text-right">
                    {player.runs}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        <div className="mt-10">

          <h3 className="mb-5 text-2xl font-bold">
            Top Wicket Takers
          </h3>

          <table className="w-full">

            <thead>

              <tr className="border-b border-slate-700">
                <th className="py-3 text-left">
                  Bowler
                </th>

                <th className="text-right">
                  Wickets
                </th>
              </tr>

            </thead>

            <tbody>

              {topBowlers.map((bowler) => (

                <tr
                  key={bowler.bowler}
                  className="border-b border-slate-700"
                >

                  <td className="py-3">
                    {bowler.bowler}
                  </td>

                  <td className="text-right">
                    {bowler.wickets}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default TeamProfile;