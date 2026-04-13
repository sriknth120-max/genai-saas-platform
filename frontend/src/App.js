import React, { useState } from "react";

function App() {
  const [token, setToken] = useState("");   // ✅ only once
  const [res, setRes] = useState("");

  const login = async () => {
    try {
      const r = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: "admin",
          password: "admin"
        })
      });

      const data = await r.json();
      console.log("Token:", data.token);

      setToken(data.token);   // ✅ store token
      alert("Login Success");

    } catch (err) {
      console.error(err);
      alert("Login Failed");
    }
  };

  const run = async () => {
    try {
      const r = await fetch(`http://127.0.0.1:8000/analyze?token=${token}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          value: Math.random() * 10
        })
      });

      const d = await r.json();
      setRes(JSON.stringify(d, null, 2));

    } catch (err) {
      console.error(err);
      alert("Error calling API");
    }
  };

  return (
    <div>
      <h1>Final GenAI SaaS</h1>
      <button onClick={login}>Login</button>
      <button onClick={run}>Run AI</button>
      <pre>{res}</pre>
    </div>
  );
}

export default App;