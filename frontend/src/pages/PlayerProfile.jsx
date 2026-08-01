import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

function PlayerProfile() {
  const { playerId } = useParams();

  const [player, setPlayer] = useState(null);

  useEffect(() => {
    api
      .get(`/players/${playerId}`)
      .then((response) => {
        setPlayer(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [playerId]);

  if (!player) {
    return (
      <div className="text-white text-2xl">
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

        <p className="mb-4 text-xl">
          <strong>Player Name:</strong> {player.player_name}
        </p>

        <p className="text-xl">
          <strong>Player ID:</strong> {player.player_id}
        </p>

      </div>

    </div>
  );
}

export default PlayerProfile;