import { useNavigate } from "react-router-dom";

function PlayerTable({ players }) {

  const navigate = useNavigate();

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700">

      <table className="min-w-full">

        <thead className="bg-slate-800">
          <tr>
            <th className="px-6 py-4 text-left">
              Player ID
            </th>

            <th className="px-6 py-4 text-left">
              Player Name
            </th>
          </tr>
        </thead>

        <tbody>

          {players.map((player) => (

            <tr
              key={player.player_id}
              onClick={() => navigate(`/players/${player.player_id}`)}
              className="cursor-pointer border-t border-slate-700 hover:bg-slate-800"
            >

              <td className="px-6 py-4 font-mono">
                {player.player_id}
              </td>

              <td className="px-6 py-4">
                {player.player_name}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default PlayerTable;