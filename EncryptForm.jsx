import React, { useState } from "react";
import axios from "axios";

const EncryptForm = () => {
  const [file, setFile] = useState(null);
  const [key, setKey] = useState("");
  const [encryptedFile, setEncryptedFile] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleEncrypt = async () => {
    if (!file || !key) {
      setError("File and key are required.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("key", key);

    try {
      const response = await axios.post("http://127.0.0.1:5000/encrypt/file", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setEncryptedFile(response.data.encrypted_file);
      setError("");  // Clear error if successful
    } catch (err) {
      setError("Encryption failed. Please try again.");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>🔒 AES File Encryption</h2>
      <input type="file" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Enter key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
      />
      <button onClick={handleEncrypt}>Encrypt</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {encryptedFile && (
        <div>
          <h3>Encrypted File:</h3>
          <a href={`http://127.0.0.1:5000/uploads/${encryptedFile}`} download>
            Download Encrypted File
          </a>
        </div>
      )}
    </div>
  );
};

export default EncryptForm;
