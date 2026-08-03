import { useNavigate } from "react-router-dom";
import TEAM_LOGOS from "../utils/teamLogos";

function TeamTable({ teams }) {
  const navigate = useNavigate();

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700">

      <table className="min-w-full">

        <thead className="bg-slate-800">
          <tr>
            <th className="px-6 py-4 text-left">
              Team
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

                <div className="flex items-center gap-4">

                  <img
                    src={TEAM_LOGOS[team.team_name]}
                    alt={team.team_name}
                    className="h-10 w-10 object-contain"
                  />

                  <span className="font-medium">
                    {team.team_name}
                  </span>

                </div>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default TeamTable; 