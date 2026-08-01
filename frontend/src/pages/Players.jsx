import { useEffect, useMemo, useState } from "react";
import api from "../services/api";
import PlayerTable from "../components/PlayerTable";
import SearchBar from "../components/SearchBar";

function Players() {
  const [players, setPlayers] = useState([]);
  const [search, setSearch] = useState("");
  const [ascending, setAscending] = useState(true);

  useEffect(() => {
    api
      .get("/players")
      .then((response) => {
        setPlayers(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const filteredPlayers = useMemo(() => {
    const filtered = players.filter((player) =>
      player.player_name.toLowerCase().includes(search.toLowerCase())
    );

    filtered.sort((a, b) => {
      if (ascending) {
        return a.player_name.localeCompare(b.player_name);
      }

      return b.player_name.localeCompare(a.player_name);
    });

    return filtered;
  }, [players, search, ascending]);

  return (
    <div className="text-white">
      <h1 className="mb-2 text-5xl font-bold">Players</h1>

      <p className="mb-6 text-slate-400">
        Total Players: {filteredPlayers.length}
      </p>

      <div className="mb-6 flex items-center gap-4">
        <div className="flex-1">
          <SearchBar
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search player..."
          />
        </div>

        <button
          onClick={() => setAscending(!ascending)}
          className="rounded-lg bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-700"
        >
          {ascending ? "A → Z" : "Z → A"}
        </button>
      </div>

      <PlayerTable players={filteredPlayers} />
    </div>
  );
}

export default Players;