import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import api from "../services/api";

function MatchScorecard() {
  const { matchId } = useParams();

  const [scorecard, setScorecard] = useState(null);

  useEffect(() => {
    api
      .get(`/matches/${matchId}/scorecard`)
      .then((res) => {
        setScorecard(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [matchId]);

  if (!scorecard) {
    return (
      <div className="text-white text-2xl">
        Loading...
      </div>
    );
  }

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Match Scorecard
      </h1>

      <div className="mb-10 rounded-xl bg-slate-800 p-6">

        <h2 className="text-3xl font-bold">
          {scorecard.match.team_1} vs {scorecard.match.team_2}
        </h2>

        <p className="mt-2">
          Winner: {scorecard.match.match_winner}
        </p>

        <p>
          Venue: {scorecard.match.venue}
        </p>

        <p>
          Season: {scorecard.match.season}
        </p>

      </div>

      <div className="rounded-xl bg-slate-800 p-6">

        <h2 className="mb-5 text-3xl font-bold">
          Batting Scorecard
        </h2>

        <table className="w-full">

          <thead>

            <tr className="border-b border-slate-700">
              <th className="py-3 text-left">Batter</th>
              <th>Runs</th>
              <th>Balls</th>
            </tr>

          </thead>

          <tbody>

            {scorecard.batting.map((player) => (

              <tr
                key={player.batter}
                className="border-b border-slate-700"
              >
                <td className="py-3">{player.batter}</td>
                <td>{player.runs}</td>
                <td>{player.balls}</td>
              </tr>

            ))}

          </tbody>

        </table>

      </div>

      <div className="mt-10 rounded-xl bg-slate-800 p-6">

        <h2 className="mb-5 text-3xl font-bold">
          Wickets
        </h2>

        <table className="w-full">

          <thead>

            <tr className="border-b border-slate-700">
              <th className="py-3 text-left">Batter Out</th>
              <th>Bowler</th>
              <th>Dismissal</th>
            </tr>

          </thead>

          <tbody>

            {scorecard.wickets.map((wicket, index) => (

              <tr
                key={index}
                className="border-b border-slate-700"
              >
                <td className="py-3">{wicket.batter_out}</td>
                <td>{wicket.bowler}</td>
                <td>{wicket.kind_of_wicket}</td>
              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default MatchScorecard;