import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import api from "../services/api";

function PlayerProfile() {
  const { playerId } = useParams();

  const [career, setCareer] = useState(null);
  const [recentInnings, setRecentInnings] = useState([]);
  const [progression, setProgression] = useState([]);
  const [opponents, setOpponents] = useState([]);
  const [seasonStats, setSeasonStats] = useState([]);
  const [venues, setVenues] = useState([]);

  useEffect(() => {
    api
      .get(`/players/${playerId}/career`)
      .then((res) => {
        setCareer(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/players/${playerId}/recent-innings`)
      .then((res) => {
        setRecentInnings(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/players/${playerId}/career-progression`)
      .then((res) => {

        let cumulativeRuns = 0;

        const chartData = res.data.map((match, index) => {

          cumulativeRuns += match.runs;

          return {
            match: index + 1,
            season: match.season,
            runs: cumulativeRuns,
          };

        });

        setProgression(chartData);

      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/players/${playerId}/opponents`)
      .then((res) => {
        setOpponents(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

    api
      .get(`/players/${playerId}/season-stats`)
      .then((res) => {
        setSeasonStats(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
    api
      .get(`/players/${playerId}/venues`)
      .then((res) => {
        setVenues(res.data);
      })
      .catch((err) => {
        console.error(err);
      });

  }, [playerId]);

  if (!career) {
    return (
      <div className="text-2xl text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="text-white">

      <h1 className="mb-8 text-5xl font-bold">
        Player Profile
      </h1>

      <div className="rounded-xl bg-slate-800 p-8">

        <h2 className="mb-2 text-3xl font-semibold">
          {career.player_name}
        </h2>

        <p className="mb-8 text-slate-400">
          Player ID: {career.player_id}
        </p>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Matches
            </p>

            <p className="text-3xl font-bold">
              {career.matches}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Runs
            </p>

            <p className="text-3xl font-bold">
              {career.runs}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Highest Score
            </p>

            <p className="text-3xl font-bold">
              {career.highest_score}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Average
            </p>

            <p className="text-3xl font-bold">
              {career.average}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Strike Rate
            </p>

            <p className="text-3xl font-bold">
              {career.strike_rate}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-slate-300">
              Not Outs
            </p>

            <p className="text-3xl font-bold">
              {career.not_outs}
            </p>
          </div>

        </div>

        <div className="mt-10">

          <h3 className="mb-5 text-2xl font-bold">
            Career Milestones
          </h3>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

            <div className="rounded-lg bg-slate-700 p-4">
              <p className="text-slate-300">
                💯 Hundreds
              </p>

              <p className="text-3xl font-bold">
                {career.hundreds}
              </p>
            </div>

            <div className="rounded-lg bg-slate-700 p-4">
              <p className="text-slate-300">
                🏏 Fifties
              </p>

              <p className="text-3xl font-bold">
                {career.fifties}
              </p>
            </div>

            <div className="rounded-lg bg-slate-700 p-4">
              <p className="text-slate-300">
                🔥 30+ Scores
              </p>

              <p className="text-3xl font-bold">
                {career.thirties}
              </p>
            </div>

            <div className="rounded-lg bg-slate-700 p-4">
              <p className="text-slate-300">
                ❌ Ducks
              </p>

              <p className="text-3xl font-bold">
                {career.ducks}
              </p>
            </div>

            <div className="rounded-lg bg-slate-700 p-4">
              <p className="text-slate-300">
                4️⃣ Fours
              </p>

              <p className="text-3xl font-bold">
                {career.fours}
              </p>
            </div>

            <div className="rounded-lg bg-slate-700 p-4">
              <p className="text-slate-300">
                6️⃣ Sixes
              </p>

              <p className="text-3xl font-bold">
                {career.sixes}
              </p>
            </div>
            <div className="mt-10">

  <h3 className="mb-5 text-2xl font-bold">
    Batting Breakdown
  </h3>

  <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

    <div className="rounded-lg bg-slate-700 p-4">
      <p className="text-slate-300">🎯 Dot Balls</p>
      <p className="text-3xl font-bold">
        {career.dot_balls}
      </p>
    </div>

    <div className="rounded-lg bg-slate-700 p-4">
      <p className="text-slate-300">1️⃣ Singles</p>
      <p className="text-3xl font-bold">
        {career.singles}
      </p>
    </div>

    <div className="rounded-lg bg-slate-700 p-4">
      <p className="text-slate-300">2️⃣ Doubles</p>
      <p className="text-3xl font-bold">
        {career.doubles}
      </p>
    </div>

    <div className="rounded-lg bg-slate-700 p-4">
      <p className="text-slate-300">3️⃣ Triples</p>
      <p className="text-3xl font-bold">
        {career.triples}
      </p>
    </div>

    <div className="rounded-lg bg-slate-700 p-4">
      <p className="text-slate-300">📈 Boundary %</p>
      <p className="text-3xl font-bold">
        {career.boundary_percentage}%
      </p>
    </div>

    <div className="rounded-lg bg-slate-700 p-4">
      <p className="text-slate-300">⚡ Balls / Boundary</p>
      <p className="text-3xl font-bold">
        {career.balls_per_boundary}
      </p>
    </div>

  </div>

</div>

          </div>

        </div>

        <div className="mt-10">

          <h3 className="mb-5 text-2xl font-bold">
            Career Runs Progression
          </h3>

          <div className="rounded-xl bg-slate-700 p-6">

            <ResponsiveContainer
              width="100%"
              height={350}
            >

              <LineChart data={progression}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                  dataKey="match"
                  tickCount={8}
                />

                <YAxis
                  domain={[0, "dataMax + 500"]}
                />

                <Tooltip
                  formatter={(value) => [`${value} Runs`, "Career Runs"]}
                  labelFormatter={(value) => `Match ${value}`}
                />

                <Line
                  type="natural"
                  dataKey="runs"
                  stroke="#3b82f6"
                  strokeWidth={3}
                  dot={false}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </div>

        <div className="mt-10">

          <h3 className="mb-5 text-2xl font-bold">
            Recent Innings
          </h3>

          <div className="overflow-x-auto rounded-lg">

            <table className="w-full">

              <thead>

                <tr className="border-b border-slate-700">

                  <th className="py-3 text-left">
                    Season
                  </th>

                  <th className="text-left">
                    Opponent
                  </th>

                  <th className="text-right">
                    Runs
                  </th>

                  <th className="text-right">
                    Balls
                  </th>

                  <th className="text-right">
                    Strike Rate
                  </th>

                  <th className="text-center">
                    Status
                  </th>

                </tr>

              </thead>

              <tbody>

                {recentInnings.map((inning, index) => (

                  <tr
                    key={index}
                    className="border-b border-slate-700 hover:bg-slate-700/30"
                  >

                    <td className="py-3">
                      {inning.season}
                    </td>

                    <td>
                      {inning.opponent}
                    </td>

                    <td className="text-right font-semibold">

                      {inning.runs}
                      {!inning.out && "*"}

                    </td>

                    <td className="text-right">
                      {inning.balls_faced}
                    </td>

                    <td className="text-right">
                      {inning.strike_rate}
                    </td>

                    <td className="text-center">

                      {inning.out ? (
                        <span className="text-red-400">
                          Out
                        </span>
                      ) : (
                        <span className="font-semibold text-green-400">
                          Not Out
                        </span>
                      )}

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </div>
        <div className="mt-10">

        <h3 className="mb-5 text-2xl font-bold">
          Opponent Statistics
        </h3>

        <div className="overflow-x-auto rounded-lg">

          <table className="w-full">

            <thead>

              <tr className="border-b border-slate-700">

                <th className="py-3 text-left">
                  Opponent
                </th>

                <th className="text-right">
                  Matches
                </th>

                <th className="text-right">
                  Runs
                </th>

                <th className="text-right">
                  Average
                </th>

                <th className="text-right">
                  Strike Rate
                </th>

              </tr>

            </thead>

            <tbody>

              {opponents.map((team) => (

                <tr
                  key={team.opponent}
                  className="border-b border-slate-700 hover:bg-slate-700/30"
                >

                  <td className="py-3">
                    {team.opponent}
                  </td>

                  <td className="text-right">
                    {team.matches}
                  </td>

                  <td className="text-right font-semibold">
                    {team.runs}
                  </td>

                  <td className="text-right">
                    {team.average}
                  </td>

                  <td className="text-right">
                    {team.strike_rate}
                  </td>

                </tr>

              ))}

      </tbody>

    </table>

  </div>

</div>
<div className="mt-10">

  <h3 className="mb-5 text-2xl font-bold">
    Season-wise Performance
  </h3>

  <div className="overflow-x-auto rounded-lg">

    <table className="w-full">

      <thead>

        <tr className="border-b border-slate-700">

          <th className="py-3 text-left">Season</th>
          <th className="text-right">Matches</th>
          <th className="text-right">Runs</th>
          <th className="text-right">HS</th>
          <th className="text-right">Avg</th>
          <th className="text-right">SR</th>
          <th className="text-right">100s</th>
          <th className="text-right">50s</th>

        </tr>

      </thead>

      <tbody>

        {seasonStats.map((season) => (

          <tr
            key={season.season}
            className="border-b border-slate-700 hover:bg-slate-700/30"
          >

            <td className="py-3 font-semibold">
              {season.season}
            </td>

            <td className="text-right">
              {season.matches}
            </td>

            <td className="text-right font-bold">
              {season.runs}
            </td>

            <td className="text-right">
              {season.highest_score}
            </td>

            <td className="text-right">
              {season.average}
            </td>

            <td className="text-right">
              {season.strike_rate}
            </td>

            <td className="text-right">
              {season.hundreds}
            </td>

            <td className="text-right">
              {season.fifties}
            </td>

          </tr>

        ))}

      </tbody>

    </table>

  </div>

</div>
<div className="mt-10">

  <h3 className="mb-5 text-2xl font-bold">
    Venue Statistics
  </h3>

  <div className="overflow-x-auto rounded-lg">

    <table className="w-full">

      <thead>

        <tr className="border-b border-slate-700">

          <th className="py-3 text-left">Venue</th>
          <th className="text-right">Matches</th>
          <th className="text-right">Runs</th>
          <th className="text-right">HS</th>
          <th className="text-right">Avg</th>
          <th className="text-right">SR</th>

        </tr>

      </thead>

      <tbody>

        {venues.map((venue, index) => (

          <tr
            key={index}
            className="border-b border-slate-700 hover:bg-slate-700/30"
          >

            <td className="py-3">{venue.venue}</td>
            <td className="text-right">{venue.matches}</td>
            <td className="text-right">{venue.runs}</td>
            <td className="text-right">{venue.highest_score}</td>
            <td className="text-right">{venue.average}</td>
            <td className="text-right">{venue.strike_rate}</td>

          </tr>

        ))}

      </tbody>

    </table>

  </div>

</div>

      </div>

    </div>
  );
}

export default PlayerProfile;