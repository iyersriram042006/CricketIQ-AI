import { useEffect, useState } from "react";
import api from "../services/api";

function TeamSearch({ onSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query.trim().length < 2) {
      setResults([]);
      return;
    }

    const timeout = setTimeout(() => {
      setLoading(true);

      api
        .get("/teams/search", {
          params: {
            q: query,
          },
        })
        .then((res) => {
          setResults(res.data);
        })
        .catch(console.error)
        .finally(() => {
          setLoading(false);
        });
    }, 300);

    return () => clearTimeout(timeout);
  }, [query]);

  return (
    <div className="relative w-full">
      <input
        type="text"
        placeholder="Search team..."
        className="w-full rounded-lg bg-slate-800 p-3 text-white outline-none focus:ring-2 focus:ring-blue-500"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {loading && (
        <div className="absolute mt-1 w-full rounded-lg bg-slate-800 p-3 text-sm text-gray-400">
          Searching...
        </div>
      )}

      {!loading && results.length > 0 && (
        <div className="absolute z-50 mt-1 max-h-64 w-full overflow-y-auto rounded-lg border border-slate-700 bg-slate-800 shadow-xl">
          {results.map((team) => (
            <button
              key={team.team_name}
              type="button"
              className="block w-full px-4 py-3 text-left hover:bg-slate-700"
              onClick={() => {
                setQuery(team.team_name);
                setResults([]);
                onSelect(team.team_name);
              }}
            >
              {team.team_name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default TeamSearch;