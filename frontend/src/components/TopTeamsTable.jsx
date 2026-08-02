import { useEffect, useState } from "react";
import api from "../services/api";

function TopTeamsTable() {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    api
      .get("/analytics/top-teams")
      .then((res) => {
        setTeams(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div className="rounded-xl bg-gray-900 p-6">

      <h2 className="mb-6 text-3xl font-bold">
        Top Teams
      </h2>

      <table className="w-full">

        <thead>

          <tr className="border-b border-gray-700">
            <th className="py-3 text-left">#</th>
            <th className="text-left">Team</th>
            <th className="text-right">Wins</th>
          </tr>

        </thead>

        <tbody>

          {teams.map((team, index) => (

            <tr
              key={team.team}
              className="border-b border-gray-800 hover:bg-gray-800"
            >

              <td className="py-3">
                {index + 1}
              </td>

              <td>
                {team.team}
              </td>

              <td className="text-right">
                {team.wins}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default TopTeamsTable;