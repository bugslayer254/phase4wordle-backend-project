import React from "react";
import "./Grid.css";

function Grid({ guesses, currentGuess, getColors }) {
  const totalRows = 6;
  const wordLength = 5;

  return (
    <div className="grid">
      {Array.from({ length: totalRows }).map((_, rowIndex) => {
        let row = "";
        let colors = [];

        if (rowIndex < guesses.length) {
          row = guesses[rowIndex];
          colors = getColors(row);
        } else if (rowIndex === guesses.length) {
          row = currentGuess;
        }

        return (
          <div key={rowIndex} className="row">
            {Array.from({ length: wordLength }).map((_, colIndex) => (
              <div
                key={colIndex}
                className="cell"
                style={{ backgroundColor: colors[colIndex] || "white" }}
              >
                {row[colIndex] || ""}
              </div>
            ))}
          </div>
        );
      })}
    </div>
  );
}

export default Grid;
