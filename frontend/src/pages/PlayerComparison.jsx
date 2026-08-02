import { useEffect, useState } from "react";
import api from "../services/api";
import PlayerSearch from "../components/PlayerSearch";

function PlayerComparison() {
  const [player1, setPlayer1] = useState("");
  const [player2, setPlayer2] = useState("");

  const [players, setPlayers] = useState([]);

  useEffect(() => {
    setPlayer1("");
    setPlayer2("");
  }, []);

  const comparePlayers = () => {
    if (!player1 || !player2) return;

    api
      .get("/player-comparison", {
        params: {
          player1,
          player2,
        },
      })
      .then((res) => {
        setPlayers(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  };

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Player Comparison
      </h1>

      <div className="mb-8 grid gap-4 md:grid-cols-3">

        <PlayerSearch
          onSelect={setPlayer1}
        />

        <PlayerSearch
          onSelect={setPlayer2}
        />

        <button
          onClick={comparePlayers}
          disabled={!player1 || !player2}
          className="rounded-lg bg-blue-600 px-6 py-3 hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-600"
        >
          Compare
        </button>

      </div>

      {players.length > 0 && (

        <table className="w-full">

          <thead>

            <tr className="border-b border-slate-700">
              <th className="py-3 text-left">Player</th>
              <th className="text-right">Runs</th>
              <th className="text-right">Balls</th>
              <th className="text-right">4s</th>
              <th className="text-right">6s</th>
              <th className="text-right">SR</th>
            </tr>

          </thead>

          <tbody>

            {players.map((player) => (

              <tr
                key={player.player_id}
                className="border-b border-slate-700"
              >

                <td className="py-3">
                  {player.player_name}
                </td>

                <td className="text-right">
                  {player.runs}
                </td>

                <td className="text-right">
                  {player.balls_faced}
                </td>

                <td className="text-right">
                  {player.fours}
                </td>

                <td className="text-right">
                  {player.sixes}
                </td>

                <td className="text-right">
                  {player.strike_rate}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      )}

    </div>
  );
}

export default PlayerComparison;