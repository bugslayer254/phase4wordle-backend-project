import React, { useState } from "react";
import Rules from "./components/Rules";
import Board from "./components/Board";
import Keyboard from "./components/Keyboard";
import EndMessage from "./components/EndMessage";
import "./App.css";

const MAX_GUESSES = 6;
const SECRET_WORD = "REACT"; // later, can come from backend/team mate’s logic

function App() {
  const [guesses, setGuesses] = useState([]); // store guesses
  const [currentGuess, setCurrentGuess] = useState("");
  const [gameOver, setGameOver] = useState(false);
  const [win, setWin] = useState(false);

  const handleKeyPress = (letter) => {
    if (gameOver) return;

    if (letter === "ENTER") {
      if (currentGuess.length === SECRET_WORD.length) {
        const newGuesses = [...guesses, currentGuess];
        setGuesses(newGuesses);
        if (currentGuess === SECRET_WORD) {
          setWin(true);
          setGameOver(true);
        } else if (newGuesses.length === MAX_GUESSES) {
          setGameOver(true);
        }
        setCurrentGuess("");
      }
    } else if (letter === "DEL") {
      setCurrentGuess(currentGuess.slice(0, -1));
    } else if (currentGuess.length < SECRET_WORD.length) {
      setCurrentGuess(currentGuess + letter);
    }
  };

  return (
    <div className="app">
      <h1>Wordle Clone</h1>
      <Rules />
      <Board guesses={guesses} secret={SECRET_WORD} currentGuess={currentGuess} />
      <Keyboard onKeyPress={handleKeyPress} />
      {gameOver && <EndMessage win={win} secret={SECRET_WORD} />}
    </div>
  );
}

export default App;
