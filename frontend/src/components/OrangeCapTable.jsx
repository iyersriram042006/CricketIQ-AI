import { useEffect, useState } from "react";
import api from "../services/api";

function OrangeCapTable() {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    api.get("/analytics/orange-cap")
      .then((res) => {
        setPlayers(res.data);
      })
      .catch(console.error);
  }, []);

  return (
    <div className="rounded-xl bg-gray-900 p-6">

      <h2 className="mb-6 text-3xl font-bold">
        🟠 Orange Cap
      </h2>

      <table className="w-full">

        <thead>
          <tr className="border-b border-gray-700">
            <th className="py-3 text-left">#</th>
            <th className="text-left">Player</th>
            <th className="text-right">Runs</th>
          </tr>
        </thead>

        <tbody>

          {players.map((player, index) => (

            <tr
              key={player.batter}
              className="border-b border-gray-800"
            >
              <td className="py-3">{index + 1}</td>
              <td>{player.batter}</td>
              <td className="text-right">{player.runs}</td>
            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default OrangeCapTable;