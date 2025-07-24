import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [chain, setChain] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/chain")
      .then((res) => setChain(res.data.chain))
      .catch((err) => console.error("API Error:", err));
  }, []);

  return (
    <div className="App">
      <h1>🛡️ CivChain - Disaster Survivor Chain</h1>
      {chain.map((block, index) => (
        <div key={index} className="block">
          <p><strong>Index:</strong> {block.index}</p>
          <p><strong>Timestamp:</strong> {block.timestamp}</p>
          <p><strong>Survivor Name:</strong> {block.data.name}</p>
          <p><strong>Status:</strong> {block.data.status}</p>
          <p><strong>Notes:</strong> {block.data.notes}</p>
          <p><strong>Previous Hash:</strong> {block.previous_hash}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
