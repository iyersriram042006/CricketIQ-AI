function StatsCard({ title, value }) {
  return (
    <div className="rounded-xl bg-slate-800 p-6 shadow-lg">
      <p className="text-slate-400 text-lg">
        {title}
      </p>

      <h2 className="mt-3 text-4xl font-bold text-white">
        {value}
      </h2>
    </div>
  );
}

export default StatsCard;