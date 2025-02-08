import React from "react";
import EncryptForm from "./components/EncryptForm";
import DecryptForm from "./components/DecryptForm";
import "./index.css"; // Import the CSS file

function App() {
  return (
    <div className="App">
      <h1>🔐 Data Encryption and Decryption Service</h1>
      <div className="container">
        <EncryptForm />
      </div>
      <br />
      <div className="container">
        <DecryptForm />
      </div>
    </div>
  );
}

export default App;
