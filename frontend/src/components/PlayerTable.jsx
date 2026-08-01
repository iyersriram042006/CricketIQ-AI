function PlayerTable({ players }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700">
      <table className="min-w-full">
        <thead className="bg-slate-800">
          <tr>
            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">
              Player ID
            </th>

            <th className="px-6 py-4 text-left text-sm font-semibold text-slate-300">
              Player Name
            </th>
          </tr>
        </thead>

        <tbody>
          {players.map((player) => (
            <tr
              key={player.player_id}
              className="border-t border-slate-700 hover:bg-slate-800 transition-colors"
            >
              <td className="px-6 py-4 font-mono text-slate-300">
                {player.player_id}
              </td>

              <td className="px-6 py-4 text-white">
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