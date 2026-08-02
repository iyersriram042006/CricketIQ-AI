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
      <div className="text-2xl text-white">
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
          <strong>Winner:</strong> {scorecard.match.match_winner}
        </p>

        <p>
          <strong>Venue:</strong> {scorecard.match.venue}
        </p>

        <p>
          <strong>Season:</strong> {scorecard.match.season}
        </p>

      </div>

      {scorecard.innings.map((inning) => (

        <div
          key={inning.innings_number}
          className="mb-10 rounded-xl bg-slate-800 p-6"
        >

          <h2 className="text-3xl font-bold">
            {inning.batting_team}
          </h2>

          <p className="mb-6 mt-2 text-xl text-slate-300">
            {inning.runs}/{inning.wickets} ({inning.overs} overs)
          </p>

          <h3 className="mb-4 text-2xl font-semibold">
            Batting
          </h3>

          <table className="mb-8 w-full">

            <thead>

              <tr className="border-b border-slate-700">
                <th className="py-3 text-left">Batter</th>
                <th>Runs</th>
                <th>Balls</th>
              </tr>

            </thead>

            <tbody>

              {scorecard.batting
                .filter(
                  (player) =>
                    player.innings_number === inning.innings_number
                )
                .map((player) => (

                  <tr
                    key={`${inning.innings_number}-${player.batter}`}
                    className="border-b border-slate-700"
                  >
                    <td className="py-3">
                      {player.batter}
                    </td>

                    <td>{player.runs}</td>

                    <td>{player.balls}</td>
                  </tr>

                ))}

            </tbody>

          </table>

          <h3 className="mb-4 text-2xl font-semibold">
            Wickets
          </h3>

          <table className="w-full">

            <thead>

              <tr className="border-b border-slate-700">
                <th className="py-3 text-left">
                  Batter Out
                </th>

                <th>Bowler</th>

                <th>Dismissal</th>
              </tr>

            </thead>

            <tbody>

              {scorecard.wickets
                .filter(
                  (wicket) =>
                    wicket.innings_number === inning.innings_number
                )
                .map((wicket, index) => (

                  <tr
                    key={`${inning.innings_number}-${index}`}
                    className="border-b border-slate-700"
                  >
                    <td className="py-3">
                      {wicket.batter_out}
                    </td>

                    <td>{wicket.bowler}</td>

                    <td>{wicket.kind_of_wicket}</td>
                  </tr>

                ))}

            </tbody>

          </table>

        </div>

      ))}

    </div>
  );
}

export default MatchScorecard;