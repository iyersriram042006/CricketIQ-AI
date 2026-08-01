import { LayoutDashboard, Users, Trophy, BarChart3 } from "lucide-react";
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-900 border-r border-slate-800">

      <div className="p-6">
        <h1 className="text-2xl font-bold text-white">
          🏏 CricketIQ AI
        </h1>
      </div>

      <nav className="px-4 space-y-2">

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