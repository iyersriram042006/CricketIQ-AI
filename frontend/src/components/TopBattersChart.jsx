import { useEffect, useState } from "react";
import api from "../services/api";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function TopBattersChart() {
  const [data, setData] = useState([]);
  const [limit, setLimit] = useState(10);

  useEffect(() => {
    api
      .get(`/analytics/top-batters?limit=${limit}`)
      .then((res) => {
        setData(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [limit]);

  return (
    <div className="mt-10 rounded-xl bg-gray-900 p-6">

      <div className="mb-6 flex items-center justify-between">

        <h2 className="text-3xl font-bold">
          Top Run Scorers
        </h2>

        <div className="flex items-center gap-3">

          <span>Show</span>

          <select
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="rounded-lg bg-slate-800 px-3 py-2 text-white"
          >
            <option value={5}>Top 5</option>
            <option value={10}>Top 10</option>
            <option value={20}>Top 20</option>
          </select>

        </div>

      </div>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <XAxis dataKey="batter" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="runs" />
        </BarChart>
      </ResponsiveContainer>

    </div>
  );
}

export default TopBattersChart;