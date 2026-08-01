import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-slate-900 border-b border-slate-700">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-4">

        <h1 className="text-3xl font-bold text-white">
          🏏 CricketIQ AI
        </h1>

        <div className="flex gap-8 text-lg text-slate-300">
          <Link className="hover:text-blue-400" to="/">
            Dashboard
          </Link>

          <Link className="hover:text-blue-400" to="/players">
            Players
          </Link>

          <Link className="hover:text-blue-400" to="/matches">
            Matches
          </Link>

          <Link className="hover:text-blue-400" to="/analytics">
            Analytics
          </Link>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;