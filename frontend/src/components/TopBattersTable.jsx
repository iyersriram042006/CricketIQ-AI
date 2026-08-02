import { useEffect, useState } from "react";
import api from "../services/api";

function TopBattersTable() {
  const [batters, setBatters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    api
      .get("/analytics/top-batters")
      .then((res) => {
        setBatters(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="rounded-xl bg-gray-900 p-6 text-white">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl bg-red-900 p-6 text-white">
        Failed to load top batters.
      </div>
    );
  }

  return (
    <div className="rounded-xl bg-gray-900 p-6">

      <h2 className="mb-6 text-3xl font-bold">
        Top 10 Batters
      </h2>

      <table className="w-full">

        <thead>

          <tr className="border-b border-gray-700">
            <th className="py-3 text-left">#</th>
            <th className="text-left">Player</th>
            <th className="text-right">Runs</th>
            <th className="text-right">Balls</th>
            <th className="text-right">4s</th>
            <th className="text-right">6s</th>
            <th className="text-right">SR</th>
          </tr>

        </thead>

        <tbody>

          {batters.map((player, index) => (

            <tr
              key={player.batter}
              className="border-b border-gray-800 hover:bg-gray-800"
            >
              <td className="py-3">{index + 1}</td>

              <td>{player.batter}</td>

              <td className="text-right">
                {player.runs.toLocaleString()}
              </td>

              <td className="text-right">
                {player.balls_faced.toLocaleString()}
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

    </div>
  );
}

export default TopBattersTable;