import React from "react";

function EndMessage({ win, secret }) {
  return (
    <div className="end-message">
      {win ? (
        <h2>🎉 Congratulations! You guessed the word!</h2>
      ) : (
        <h2>😢 Game Over! The word was <strong>{secret}</strong></h2>
      )}
    </div>
  );
}

export default EndMessage;
