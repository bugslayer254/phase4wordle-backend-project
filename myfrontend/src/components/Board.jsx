import React from "react";
import GuessRow from "./GuessRow";

function Board({ guesses, secret, currentGuess }) {
  return (
    <div className="board">
      {guesses.map((guess, i) => (
        <GuessRow key={i} guess={guess} secret={secret} />
      ))}
      {/* Show the current guess being typed */}
      {guesses.length < 6 && (
        <GuessRow guess={currentGuess} secret={secret} isCurrent />
      )}
    </div>
  );
}

export default Board;
