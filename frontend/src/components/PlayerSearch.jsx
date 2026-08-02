import { useEffect, useState } from "react";
import api from "../services/api";

function PlayerSearch({ onSelect }) {
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
        .get("/players/search", {
          params: {
            q: query,
          },
        })
        .then((res) => {
          setResults(res.data);
        })
        .catch((err) => {
          console.error(err);
        })
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
        placeholder="Search player..."
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

          {results.map((player) => (
            <button
              key={player.player_id}
              type="button"
              className="block w-full px-4 py-3 text-left hover:bg-slate-700"
              onClick={() => {
                setQuery(player.player_name);
                setResults([]);
                onSelect(player.player_id);
              }}
            >
              {player.player_name}
            </button>
          ))}

        </div>
      )}

    </div>
  );
}

export default PlayerSearch;