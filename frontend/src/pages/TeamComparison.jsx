import { useEffect, useState } from "react";
import api from "../services/api";

function TeamComparison() {
  const [teams, setTeams] = useState([]);

  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");

  const [result, setResult] = useState(null);

  useEffect(() => {
    api
      .get("/teams")
      .then((res) => {
        setTeams(res.data);

        if (res.data.length >= 2) {
          setTeam1(res.data[0].team_name);
          setTeam2(res.data[1].team_name);
        }
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  const compareTeams = () => {
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

        <select
          className="rounded-lg bg-slate-800 p-3"
          value={team1}
          onChange={(e) => setTeam1(e.target.value)}
        >
          {teams.map((team) => (
            <option
              key={team.team_id}
              value={team.team_name}
            >
              {team.team_name}
            </option>
          ))}
        </select>

        <select
          className="rounded-lg bg-slate-800 p-3"
          value={team2}
          onChange={(e) => setTeam2(e.target.value)}
        >
          {teams.map((team) => (
            <option
              key={team.team_id}
              value={team.team_name}
            >
              {team.team_name}
            </option>
          ))}
        </select>

        <button
          onClick={compareTeams}
          className="rounded-lg bg-blue-600 px-6 py-3 hover:bg-blue-700"
        >
          Compare
        </button>

      </div>

      {result && (

        <div className="rounded-xl bg-slate-800 p-8">

          <h2 className="mb-6 text-3xl font-bold">
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