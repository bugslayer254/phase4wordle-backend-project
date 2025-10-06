import React from "react";

const keys = [
  ..."QWERTYUIOP".split(""),
  ..."ASDFGHJKL".split(""),
  ..."ZXCVBNM".split(""),
];

function Keyboard({ onKeyPress }) {
  return (
    <div className="keyboard">
      <div className="row">
        {"QWERTYUIOP".split("").map((k) => (
          <button key={k} onClick={() => onKeyPress(k)}>{k}</button>
        ))}
      </div>
      <div className="row">
        {"ASDFGHJKL".split("").map((k) => (
          <button key={k} onClick={() => onKeyPress(k)}>{k}</button>
        ))}
      </div>
      <div className="row">
        <button onClick={() => onKeyPress("ENTER")}>ENTER</button>
        {"ZXCVBNM".split("").map((k) => (
          <button key={k} onClick={() => onKeyPress(k)}>{k}</button>
        ))}
        <button onClick={() => onKeyPress("DEL")}>DEL</button>
      </div>
    </div>
  );
}

export default Keyboard;
