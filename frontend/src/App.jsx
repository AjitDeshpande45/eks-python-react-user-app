import { useState, useEffect } from "react";

function App() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    try {
      const res = await fetch("http://13.201.86.118:30010/api/users");
      const data = await res.json();
      setUsers(data);
    } catch (err) {
      console.error("Failed to fetch users", err);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://13.201.86.118:30010/api/addusers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email })
      });

      const data = await res.json();

      if (res.ok) {
        setMessage(data.message);
        fetchUsers(); // refresh user list
      } else {
        setMessage(data.error || "Error submitting form");
      }

      setName("");
      setEmail("");
    } catch (err) {
      setMessage("Request failed: " + err.message);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h2>Create User</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name: </label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <br />
        <div>
          <label>Email: </label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} required type="email" />
        </div>
        <br />
        <button type="submit">Submit</button>
      </form>
      <br />
      {message && <p><strong>{message}</strong></p>}

      <h3>Existing Users</h3>
      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.name} — {u.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;