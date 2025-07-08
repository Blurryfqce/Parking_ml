import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [datetime, setDatetime] = useState("");
  const [percentage, setPercentage] = useState(null);
  const [error, setError] = useState(null);
  const [warning, setWarning] = useState(null);
  const [minDateTime, setMinDateTime] = useState("");
  const [maxDateTime, setMaxDateTime] = useState("");
  const [readableTime, setReadableTime] = useState("");

useEffect(() => {
  const now = new Date();

  // Round to nearest minute (remove seconds)
  now.setSeconds(0, 0);

  const in48Hours = new Date(now.getTime() + 48 * 60 * 60 * 1000);

const formatDate = (date) => {
  const pad = (n) => n.toString().padStart(2, "0");
  const yyyy = date.getFullYear();
  const mm = pad(date.getMonth() + 1);
  const dd = pad(date.getDate());
  const hh = pad(date.getHours());
  const mi = pad(date.getMinutes());
  return `${yyyy}-${mm}-${dd}T${hh}:${mi}`;
};


  setDatetime(formatDate(now));
  setMinDateTime(formatDate(now));
  setMaxDateTime(formatDate(in48Hours));
}, []);


  const handleChange = (e) => {
  const selected = e.target.value;
  setDatetime(selected);

  // Convert to readable format
  const dt = new Date(selected);
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  };
  const formatted = dt.toLocaleString(undefined, options);
  setReadableTime(formatted);

  if (selected < minDateTime || selected > maxDateTime) {
    setWarning("Please select a time within the next 48 hours.");
  } else {
    setWarning(null);
  }
};


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (datetime < minDateTime || datetime > maxDateTime) {
      setWarning("Selected time is out of range. Please pick a valid time.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ datetime }),
      });

      const data = await response.json();
      console.log("Received:", data);

      if (data.occupancy_percentage !== undefined) {
        setPercentage(data.occupancy_percentage);
        setError(null);
      } else if (data.error) {
        setError(`Error: ${data.error}`);
        setPercentage(null);
      }
    } catch (error) {
      setError("Error: Could not connect to the server");
      setPercentage(null);
    }
  };

  // Set display color based on percentage
  const getColor = () => {
    if (percentage <= 40) return "green";
    if (percentage <= 80) return "orange";
    return "red";
  };

  return (
    <div className="App">
      <h1>Predict Parking Lot Occupancy</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Select Date & Time:
          <input
            type="datetime-local"
            value={datetime}
            onChange={handleChange}
            min={minDateTime}
            max={maxDateTime}
            required
          />
        </label>
        <button type="submit">Predict</button>
      </form>
      
      {readableTime && !warning && (
        <p style={{ fontStyle: "italic", marginTop: "10px" }}>
          🕓 You selected: <strong>{readableTime}</strong>
        </p>
      )}

      {warning && (
        <p style={{ color: "orange", marginTop: "10px" }}>{warning}</p>
      )}

      {percentage !== null && !error && (
        <p
          style={{
            marginTop: "20px",
            fontSize: "24px",
            fontWeight: "bold",
            color: getColor(),
          }}
        >
          Occupancy: {percentage}%
        </p>
      )}

      {error && (
        <p style={{ marginTop: "20px", color: "red" }}>{error}</p>
      )}
    </div>
  );
}

export default App;
