import { useNavigate } from "react-router-dom";

function TeamTable({ teams }) {
  const navigate = useNavigate();

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700">

      <table className="min-w-full">

        <thead className="bg-slate-800">

          <tr>
            <th className="px-6 py-4 text-left">
              Team ID
            </th>

            <th className="px-6 py-4 text-left">
              Team Name
            </th>
          </tr>

        </thead>

        <tbody>

          {teams.map((team) => (

            <tr
              key={team.team_id}
              onClick={() =>
                navigate(`/teams/${encodeURIComponent(team.team_name)}`)
              }
              className="cursor-pointer border-t border-slate-700 hover:bg-slate-800"
            >

              <td className="px-6 py-4">
                {team.team_id}
              </td>

              <td className="px-6 py-4">
                {team.team_name}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default TeamTable;