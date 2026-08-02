import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import api from "../services/api";

function PlayerProfile() {
  const { playerId } = useParams();

  const [player, setPlayer] = useState(null);

  useEffect(() => {
    api
      .get(`/players/${playerId}/profile`)
      .then((response) => {
        setPlayer(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [playerId]);

  if (!player) {
    return (
      <div className="text-2xl text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="text-white">

      <h1 className="text-5xl font-bold">
        {player.player_name}
      </h1>

      <p className="mt-2 mb-10 text-slate-400">
        Player ID: {player.player_id}
      </p>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

        <div className="rounded-xl bg-slate-800 p-6">
          <p className="text-slate-400">Runs</p>
          <h2 className="mt-2 text-4xl font-bold">
            {player.runs ?? 0}
          </h2>
        </div>

        <div className="rounded-xl bg-slate-800 p-6">
          <p className="text-slate-400">Balls Faced</p>
          <h2 className="mt-2 text-4xl font-bold">
            {player.balls_faced ?? 0}
          </h2>
        </div>

        <div className="rounded-xl bg-slate-800 p-6">
          <p className="text-slate-400">Strike Rate</p>
          <h2 className="mt-2 text-4xl font-bold">
            {player.strike_rate ?? 0}
          </h2>
        </div>

        <div className="rounded-xl bg-slate-800 p-6">
          <p className="text-slate-400">Fours</p>
          <h2 className="mt-2 text-4xl font-bold">
            {player.fours ?? 0}
          </h2>
        </div>

        <div className="rounded-xl bg-slate-800 p-6">
          <p className="text-slate-400">Sixes</p>
          <h2 className="mt-2 text-4xl font-bold">
            {player.sixes ?? 0}
          </h2>
        </div>

      </div>

    </div>
  );
}

export default PlayerProfile;