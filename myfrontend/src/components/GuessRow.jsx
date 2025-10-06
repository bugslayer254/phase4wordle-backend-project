import React from "react";

function getFeedback(letter, index, secret) {
  if (!letter) return "";
  if (secret[index] === letter) return "correct";
  if (secret.includes(letter)) return "present";
  return "absent";
}

function GuessRow({ guess, secret, isCurrent }) {
  const letters = guess.padEnd(secret.length).split("");

  return (
    <div className="guess-row">
      {letters.map((letter, i) => (
        <div key={i} className={`tile ${isCurrent ? "current" : getFeedback(letter, i, secret)}`}>
          {letter}
        </div>
      ))}
    </div>
  );
}

export default GuessRow;
