import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

function Matches() {
  const [matches, setMatches] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/matches")
      .then((res) => {
        setMatches(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Matches
      </h1>

      <div className="space-y-4">

        {matches.map((match) => (

          <div
            key={match.match_id}
            className="rounded-xl bg-slate-800 p-6 hover:bg-slate-700 transition cursor-pointer"
            onClick={() => navigate(`/matches/${match.match_id}`)}
          >

            <h2 className="text-2xl font-bold">
              {match.team_1} vs {match.team_2}
            </h2>

            <p className="mt-2 text-slate-300">
              Season: {match.season}
            </p>

            <p className="text-slate-300">
              Venue: {match.venue}
            </p>

            <p className="text-slate-300">
              Winner: {match.match_winner}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Matches;