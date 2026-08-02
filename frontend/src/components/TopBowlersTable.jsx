import { useEffect, useState } from "react";
import api from "../services/api";

function TopBowlersTable() {

  const [bowlers, setBowlers] = useState([]);

  useEffect(() => {
    api.get("/analytics/top-bowlers")
      .then((res) => {
        setBowlers(res.data);
      });
  }, []);

  return (
    <div className="mt-10 rounded-xl bg-gray-900 p-6">

      <h2 className="mb-6 text-3xl font-bold">
        Top 10 Bowlers
      </h2>

      <table className="w-full">

        <thead>
            <tr className="border-b border-gray-700">
              <th className="py-3 text-left">#</th>
              <th className="text-left">Bowler</th>
              <th className="text-right">Matches</th>
              <th className="text-right">Wickets</th>
            </tr>
          </thead>

        <tbody>

          {bowlers.map((bowler, index) => (

            <tr
              key={bowler.bowler}
              className="border-b border-gray-800 hover:bg-gray-800"
            >

              <td className="py-3">{index + 1}</td>

              <td>{bowler.bowler}</td>

              <td className="text-right">
                {bowler.matches}
              </td>

              <td className="text-right">
                {bowler.wickets}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default TopBowlersTable;