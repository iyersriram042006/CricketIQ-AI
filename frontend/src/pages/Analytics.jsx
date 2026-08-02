import TopBattersTable from "../components/TopBattersTable";
import TopBowlersTable from "../components/TopBowlersTable";
import TopTeamsTable from "../components/TopTeamsTable";
import TopBattersChart from "../components/TopBattersChart";
import OrangeCapTable from "../components/OrangeCapTable";
import PurpleCapTable from "../components/PurpleCapTable";

function Analytics() {
  return (
    <div className="text-white">

      <h1 className="mb-10 text-5xl font-bold">
        Analytics
      </h1>

      <div className="grid gap-8 xl:grid-cols-2">

        <TopBattersTable />

        <TopBowlersTable />

      </div>

      <div className="mt-10 grid gap-8 xl:grid-cols-2">

        <OrangeCapTable />

        <PurpleCapTable />

      </div>

      <div className="mt-10">

        <TopTeamsTable />

      </div>

      <div className="mt-10">

        <TopBattersChart />

      </div>

    </div>
  );
}

export default Analytics;