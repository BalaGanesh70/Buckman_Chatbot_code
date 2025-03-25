import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!userInput.trim()) return;

    const userMessage = { role: "user", content: userInput };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      console.log("📤 Sending to backend:", userInput);

      const response = await axios.post("http://127.0.0.1:5000/chat", { query: userInput });

      console.log("📥 Received from backend:", response.data);

      if (response.data && response.data.answer) {
        const botMessage = { role: "bot", content: response.data.answer };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } else {
        console.error("⚠️ Unexpected API response:", response.data);
      }
    } catch (error) {
      console.error("❌ Error communicating with backend:", error);
    }

    setUserInput("");
  };

  return (
    <div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default Chatbot;