import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Dashboard from "./pages/Dashboard";
import Players from "./pages/Players";
import Matches from "./pages/Matches";
import Analytics from "./pages/Analytics";
import PlayerProfile from "./pages/PlayerProfile";
import MatchScorecard from "./pages/MatchScorecard";
import PlayerComparison from "./pages/PlayerComparison";
import Teams from "./pages/Teams";
import TeamProfile from "./pages/TeamProfile";
import TeamComparison from "./pages/TeamComparison";

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/players" element={<Players />} />
          <Route path="/players/:playerId" element={<PlayerProfile />} />
          <Route path="/matches" element={<Matches />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/matches/:matchId" element={<MatchScorecard />} />
          <Route path="/compare" element={<PlayerComparison />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/teams/:teamName" element={<TeamProfile />} />
          <Route path="/team-comparison" element={<TeamComparison />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;