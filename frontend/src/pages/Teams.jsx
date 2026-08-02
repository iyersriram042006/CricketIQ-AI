import { useEffect, useMemo, useState } from "react";

import api from "../services/api";
import SearchBar from "../components/SearchBar";
import TeamTable from "../components/TeamTable";

function Teams() {
  const [teams, setTeams] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    api
      .get("/teams")
      .then((res) => {
        setTeams(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  const filteredTeams = useMemo(() => {
    return teams.filter((team) =>
      team.team_name
        .toLowerCase()
        .includes(search.toLowerCase())
    );
  }, [teams, search]);

  return (
    <div className="text-white">

      <h1 className="mb-2 text-5xl font-bold">
        Teams
      </h1>

      <p className="mb-6 text-slate-400">
        Total Teams: {filteredTeams.length}
      </p>

      <div className="mb-6">

        <SearchBar
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search team..."
        />

      </div>

      <TeamTable teams={filteredTeams} />

    </div>
  );
}

export default Teams;