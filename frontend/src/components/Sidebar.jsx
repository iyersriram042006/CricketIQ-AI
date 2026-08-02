import {
  LayoutDashboard,
  Users,
  Trophy,
  BarChart3,
  Shield,
  GitCompareArrows,
} from "lucide-react";
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="w-64 min-h-screen border-r border-slate-800 bg-slate-900">

      <div className="p-6">
        <h1 className="text-2xl font-bold text-white">
          🏏 CricketIQ AI
        </h1>
      </div>

      <nav className="space-y-2 px-4">

        <Link
          to="/"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <LayoutDashboard size={20} />
          Dashboard
        </Link>

        <Link
          to="/players"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <Users size={20} />
          Players
        </Link>

        <Link
          to="/compare"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <GitCompareArrows size={20} />
          Compare Players
        </Link>

        <Link
          to="/teams"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <Shield size={20} />
          Teams
        </Link>

        <Link
          to="/team-comparison"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <GitCompareArrows size={20} />
          Team Comparison
        </Link>

        <Link
          to="/matches"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <Trophy size={20} />
          Matches
        </Link>

        <Link
          to="/analytics"
          className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-300 hover:bg-slate-800 hover:text-white"
        >
          <BarChart3 size={20} />
          Analytics
        </Link>

      </nav>

    </aside>
  );
}

export default Sidebar;