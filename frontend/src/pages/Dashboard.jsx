import { useEffect, useState } from "react";

import api from "../services/api";
import StatsCard from "../components/StatsCard";

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

      <h1 className="mb-10 text-5xl font-bold text-white">
        Dashboard
      </h1>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

        <StatsCard
          title="Matches"
          value={stats.matches}
        />

        <StatsCard
          title="Players"
          value={stats.players}
        />

        <StatsCard
          title="Teams"
          value={stats.teams}
        />

        <StatsCard
          title="Venues"
          value={stats.venues}
        />

        <StatsCard
          title="Deliveries"
          value={stats.deliveries}
        />

        <StatsCard
          title="Wickets"
          value={stats.wickets}
        />

      </div>

    </div>
  );
}

export default Dashboard;