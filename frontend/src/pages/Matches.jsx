import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

function Matches() {
  const [matches, setMatches] = useState([]);
  const [search, setSearch] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    api
      .get("/matches")
      .then((res) => {
        setMatches(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  const filteredMatches = useMemo(() => {
    const query = search.toLowerCase();

    return matches.filter((match) => {
      return (
        match.team_1.toLowerCase().includes(query) ||
        match.team_2.toLowerCase().includes(query) ||
        match.venue.toLowerCase().includes(query) ||
        String(match.season).includes(query)
      );
    });
  }, [matches, search]);

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Matches
      </h1>

      <input
        type="text"
        placeholder="Search by team, venue or season..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-8 w-full rounded-xl bg-slate-800 p-4 text-white outline-none"
      />

      <p className="mb-6 text-slate-400">
        Total Matches: {filteredMatches.length}
      </p>

      <div className="space-y-4">

        {filteredMatches.map((match) => (

          <div
            key={match.match_id}
            onClick={() => navigate(`/matches/${match.match_id}`)}
            className="cursor-pointer rounded-xl bg-slate-800 p-6 transition hover:bg-slate-700"
          >

            <h2 className="text-2xl font-bold">
              {match.team_1} vs {match.team_2}
            </h2>

            <p className="mt-2 text-slate-300">
              <strong>Season:</strong> {match.season}
            </p>

            <p className="text-slate-300">
              <strong>Venue:</strong> {match.venue}
            </p>

            <p className="text-slate-300">
              <strong>Winner:</strong> {match.match_winner}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default Matches;