import React, { useState } from 'react';
import axios from 'axios';

const ROWS = 6;
const COLS = 7;

function App() {
    const [board, setBoard] = useState(Array(ROWS).fill().map(() => Array(COLS).fill(0)));
    const [player, setPlayer] = useState(1);
    const [scores, setScores] = useState(Array(COLS).fill(0));

    const makeMove = async (column) => {
        const newRow = board.findIndex(row => row[column] === 0);
        if (newRow !== -1) {
            const newBoard = [...board];
            newBoard[newRow][column] = player;
            setBoard(newBoard);

            // Switch player
            const newPlayer = 3 - player;
            setPlayer(newPlayer);

            // Get best move from backend for Bot
            if (newPlayer === 2) {
                const response = await axios.post('http://localhost:5000/best-move', { board: newBoard });
                const bestMove = response.data.column;
                setScores(response.data.score);
                makeMove(bestMove);
            }
        }
    };

    return (
        <div>
            {/* Render the board and scores here */}
            {board.map((row, rowIndex) => (
                <div key={rowIndex}>
                    {row.map((cell, colIndex) => (
                        <button key={colIndex} onClick={() => makeMove(colIndex)}>
                            {cell === 1 ? 'X' : cell === 2 ? 'O' : ''}
                        </button>
                    ))}
                </div>
            ))}
            <div>
                {scores.map((score, index) => (
                    <span key={index}>{score}</span>
                ))}
            </div>
        </div>
    );
}

export default App;
