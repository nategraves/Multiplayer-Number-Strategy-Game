import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import './Board.css';

interface Tile {
  value: number;
  graph: number[];
}

interface Player {
  name: string;
  score: number;
}

interface BoardData {
  players: Player[];
  width: number;
  height: number;
  tiles: Tile[];
  turn: number;
  lastPlayed: number | null;
}

const Board: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [board, setBoard] = useState<BoardData | null>(null);
  const [error, setError] = useState<string>('');

  const fetchBoard = useCallback(async () => {
    try {
      const response = await fetch(`/api/game/${id}`);
      const data = await response.json();
      if (data.board) {
        setBoard(data.board);
      }
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  }, [id]);

  useEffect(() => {
    fetchBoard();
    const interval = setInterval(fetchBoard, 1500);
    return () => clearInterval(interval);
  }, [fetchBoard]);

  const playTile = async (tileIndex: number) => {
    if (!board) return;

    // Only allow playing tiles with value 0
    if (board.tiles[tileIndex].value !== 0) {
      setError('You can only play unoccupied (i.e. "0") tiles.');
      setTimeout(() => setError(''), 3000);
      return;
    }

    try {
      const response = await fetch('/api/play', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          board_id: id,
          tile: tileIndex,
        }),
      });

      const data = await response.json();
      if (data.tiles) {
        setBoard(data);
        setError('');
      } else if (data.error) {
        setError(data.error);
      }
    } catch (error) {
      console.error('Error playing tile:', error);
      setError('Failed to play tile');
    }
  };

  if (!board) {
    return <div className="container">Loading...</div>;
  }

  const currentPlayer = board.players[board.turn % board.players.length];

  return (
    <div className="container">
      <div className="row">
        <div className={`board-container span${board.width}`}>
          <h3 id="turn">{currentPlayer.name}'s turn</h3>
          {error && <h4 className="error">{error}</h4>}
          <div className="board">
            {board.tiles.map((tile, index) => (
              <button
                key={index}
                id={`tile-${index}`}
                className={`tiles val${tile.value}`}
                onClick={() => playTile(index)}
              >
                {tile.value}
              </button>
            ))}
          </div>
        </div>
        <div className="span2 scoreboard">
          {board.players.map((player, index) => (
            <p key={index}>
              <b className="name">{player.name}:</b>{' '}
              <span className="score">{player.score}</span>
            </p>
          ))}
        </div>
        <div className="span3 instructions">
          <h4>How to play:</h4>
          <p>
            The object of the game is to collect points by completing series of
            3 or more touching tiles (diagonals don't count). Click on a "0"
            tile to bump it to a one. String three or more "1" tiles together
            and you'll bump the completing tile to a "2" and reset the other
            tiles. Keep going until the board is full.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Board;
