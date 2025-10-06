import React from "react";
import "./Keyboard.css";

function Keyboard({ onKeyPress }) {
  const row1 = "QWERTYUIOP".split("");
  const row2 = "ASDFGHJKL".split("");
  const row3 = "ZXCVBNM".split("");

  return (
    <div>
      <div>
        {row1.map((k) => (
          <button
            key={k}
            onClick={() => onKeyPress(k)}
            style={{ margin: "2px" }}
          >
            {k}
          </button>
        ))}
      </div>
      <div>
        {row2.map((k) => (
          <button
            key={k}
            onClick={() => onKeyPress(k)}
            style={{ margin: "2px" }}
          >
            {k}
          </button>
        ))}
      </div>
      <div>
        <button onClick={() => onKeyPress("ENTER")} style={{ margin: "2px" }}>
          ENTER
        </button>
        {row3.map((k) => (
          <button
            key={k}
            onClick={() => onKeyPress(k)}
            style={{ margin: "2px" }}
          >
            {k}
          </button>
        ))}
        <button onClick={() => onKeyPress("BACK")} style={{ margin: "2px" }}>
          BACK
        </button>
      </div>
    </div>
  );
}

export default Keyboard;
