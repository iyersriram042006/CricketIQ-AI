import TopBattersTable from "../components/TopBattersTable";
import TopBowlersTable from "../components/TopBowlersTable";

function Analytics() {
  return (
    <div className="text-white">

      <h1 className="mb-10 text-5xl font-bold">
        Analytics
      </h1>

      <TopBattersTable />

      <TopBowlersTable />

    </div>
  );
}

export default Analytics;