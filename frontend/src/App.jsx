import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/players")
      .then((response) => {
        setPlayers(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>🏏 CricketIQ AI</h1>

      <h2>Players</h2>

      {players.map((player) => (
        <p key={player.player_id}>
          {player.player_name}
        </p>
      ))}
    </div>
  );
}

export default App;