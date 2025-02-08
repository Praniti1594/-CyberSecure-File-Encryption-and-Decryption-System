import React, { useState } from "react";
import axios from "axios";

const DecryptForm = () => {
  const [file, setFile] = useState(null);
  const [key, setKey] = useState("");
  const [decryptedFile, setDecryptedFile] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDecrypt = async () => {
    if (!file || !key) {
      setError("File and key are required.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("key", key);

    try {
      const response = await axios.post("http://127.0.0.1:5000/decrypt/file", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setDecryptedFile(response.data.decrypted_file);
      setError("");  // Clear error if successful
    } catch (err) {
      setError("Decryption failed. Please try again.");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>🔓 AES File Decryption</h2>
      <input type="file" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Enter key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
      />
      <button onClick={handleDecrypt}>Decrypt</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {decryptedFile && (
        <div>
          <h3>Decrypted File:</h3>
          <a href={`http://127.0.0.1:5000/uploads/${decryptedFile}`} download>
            Download Decrypted File
          </a>
        </div>
      )}
    </div>
  );
};

export default DecryptForm;
