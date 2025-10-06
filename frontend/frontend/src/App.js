import React, { useState } from "react";
import "./App.css";
import Grid from "./components/Grid";
import Keyboard from "./components/Keyboard";

function App() {
  const [guesses, setGuesses] = useState([]);
  const [currentGuess, setCurrentGuess] = useState("");
  const targetWord = "REACT"; // you can change this later

  function handleKeyPress(key) {
    if (key === "ENTER") {
      if (currentGuess.length === 5) {
        setGuesses([...guesses, currentGuess]); // add word to guesses
        setCurrentGuess(""); // reset for next word
      }
    } else if (key === "BACK") {
      setCurrentGuess(currentGuess.slice(0, -1)); // remove last letter
    } else {
      if (currentGuess.length < 5) {
        setCurrentGuess(currentGuess + key); // add letter
      }
    }
  }

  function getColors(guess) {
    const colors = Array(guess.length).fill("gray");

    for (let i = 0; i < guess.length; i++) {
      if (guess[i] === targetWord[i]) {
        colors[i] = "green";
      } else if (targetWord.includes(guess[i])) {
        colors[i] = "yellow";
      }
    }

    return colors;
  }

  return (
    <div className="app">
      <h1>Wordle Clone</h1>
      <Grid
        guesses={guesses}
        currentGuess={currentGuess}
        getColors={getColors}
      />
      <Keyboard onKeyPress={handleKeyPress} />
    </div>
  );
}
export default App;
