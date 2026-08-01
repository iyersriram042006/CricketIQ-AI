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

      <h1 className="mb-8 text-5xl font-bold">
        Player Profile
      </h1>

      <div className="rounded-xl bg-slate-800 p-8">

        <h2 className="mb-6 text-3xl font-semibold">
          {player.player_name}
        </h2>

        <div className="grid gap-4 md:grid-cols-2">

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-gray-300">Player ID</p>
            <p className="text-xl font-bold">
              {player.player_id}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-gray-300">Runs</p>
            <p className="text-3xl font-bold">
              {player.runs ?? 0}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-gray-300">Balls Faced</p>
            <p className="text-3xl font-bold">
              {player.balls_faced ?? 0}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-gray-300">Strike Rate</p>
            <p className="text-3xl font-bold">
              {player.strike_rate ?? 0}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-gray-300">Fours</p>
            <p className="text-3xl font-bold">
              {player.fours ?? 0}
            </p>
          </div>

          <div className="rounded-lg bg-slate-700 p-4">
            <p className="text-gray-300">Sixes</p>
            <p className="text-3xl font-bold">
              {player.sixes ?? 0}
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default PlayerProfile;