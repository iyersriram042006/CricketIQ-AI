import { useEffect, useState } from "react";
import api from "../services/api";

function PurpleCapTable() {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    api.get("/analytics/purple-cap")
      .then((res) => {
        setPlayers(res.data);
      })
      .catch(console.error);
  }, []);

  return (
    <div className="rounded-xl bg-gray-900 p-6">

      <h2 className="mb-6 text-3xl font-bold">
        🟣 Purple Cap
      </h2>

      <table className="w-full">

        <thead>
          <tr className="border-b border-gray-700">
            <th className="py-3 text-left">#</th>
            <th className="text-left">Bowler</th>
            <th className="text-right">Wickets</th>
          </tr>
        </thead>

        <tbody>

          {players.map((player, index) => (

            <tr
              key={player.bowler}
              className="border-b border-gray-800"
            >
              <td className="py-3">{index + 1}</td>
              <td>{player.bowler}</td>
              <td className="text-right">{player.wickets}</td>
            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default PurpleCapTable;