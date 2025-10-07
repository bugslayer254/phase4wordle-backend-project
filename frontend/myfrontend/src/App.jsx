import React, { useEffect, useState } from "react";
import Rules from "./components/Rules";
import Board from "./components/Board";
import Keyboard from "./components/Keyboard";
import EndMessage from "./components/EndMessage";
import Login from "./components/Login";
import "./App.css";

const MAX_GUESSES = 6;

function App() {
  const [userId, setUserId] = useState(localStorage.getItem("user_id"));
  const [secretWord, setSecretWord] = useState("");
  const [guesses, setGuesses] = useState([]); // store guesses
  const [currentGuess, setCurrentGuess] = useState("");
  const [gameOver, setGameOver] = useState(false);
  const [win, setWin] = useState(false);

  useEffect(() => {
    if (!userId) return;
    fetch("/api/words")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          const randomWord = data[Math.floor(Math.random() * data.length)].text;
          setSecretWord(randomWord);
        } else {
          console.error("No words received from backend");
        }
      })
      .catch((err) => console.error("Error fetching word:", err));
  }, [userId]);

  const handleKeyPress = (letter) => {
    if (gameOver || !secretWord) return;

    if (letter === "ENTER") {
      if (currentGuess.length === secretWord.length) {
        const newGuesses = [...guesses, currentGuess];
        setGuesses(newGuesses);
        if (currentGuess.toUpperCase() === secretWord.toUpperCase()) {
          setWin(true);
          setGameOver(true);
        } else if (newGuesses.length === MAX_GUESSES) {
          setGameOver(true);
        }
        setCurrentGuess("");
      }
    } else if (letter === "DEL") {
      setCurrentGuess(currentGuess.slice(0, -1));
    } else if (currentGuess.length < secretWord.length) {
      setCurrentGuess(currentGuess + letter);
    }
  };

  if (!userId) {
    return <Login onLogin={setUserId} />;
  }

  return (
    <div className="app">
      <h1>Wordle Clone</h1>
      <Rules />

      <button
        onClick={() => {
          setUserId(null);
          localStorage.removeItem("user_id");
        }}
        style={{ marginBottom: "10px" }}
      >
        Logout
      </button>

      <Board
        guesses={guesses}
        secret={secretWord}
        currentGuess={currentGuess}
      />
      <Keyboard onKeyPress={handleKeyPress} />
      {gameOver && <EndMessage win={win} secret={secretWord} />}
    </div>
  );
}

export default App;
