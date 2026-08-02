import { useEffect, useState } from "react";

import api from "../services/api";
import StatsCard from "../components/StatsCard";
import TopBattersTable from "../components/TopBattersTable";
import TopBowlersTable from "../components/TopBowlersTable";
import TopTeamsTable from "../components/TopTeamsTable";

function Dashboard() {

  const [stats, setStats] = useState({});

  useEffect(() => {
    api.get("/analytics/dashboard")
      .then((res) => {
        setStats(res.data);
      });
  }, []);

  return (
    <div className="text-white">

      <h1 className="mb-10 text-5xl font-bold">
        Dashboard
      </h1>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

        <StatsCard title="Matches" value={stats.matches} />
        <StatsCard title="Players" value={stats.players} />
        <StatsCard title="Teams" value={stats.teams} />
        <StatsCard title="Venues" value={stats.venues} />
        <StatsCard title="Deliveries" value={stats.deliveries} />
        <StatsCard title="Wickets" value={stats.wickets} />

      </div>

      <div className="mt-12 grid gap-8 xl:grid-cols-2">

        <TopBattersTable />

        <TopBowlersTable />

      </div>

      <div className="mt-8">
        <TopTeamsTable />
      </div>

    </div>
  );
}

export default Dashboard;