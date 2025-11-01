import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home: React.FC = () => {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [width, setWidth] = useState('3');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ player1, player2, width }),
      });

      const data = await response.json();
      if (data.boardId) {
        navigate(`/board/${data.boardId}`);
      }
    } catch (error) {
      console.error('Error creating game:', error);
    }
  };

  return (
    <div className="container">
      <div className="row">
        <div className="span4">
          <h1>Tritina</h1>
          <h2>A tricky tile game to play with friends.</h2>
        </div>
        <div className="span4 offset1">
          <form onSubmit={handleSubmit} className="form-vertical">
            <fieldset>
              <div className="control-group">
                <label className="control-label" htmlFor="player1">
                  Player 1:
                </label>
                <input
                  type="text"
                  className="input-large"
                  name="player1"
                  id="player1"
                  value={player1}
                  onChange={(e) => setPlayer1(e.target.value)}
                  required
                />
                <br className="clear" />
                <label className="control-label" htmlFor="player2">
                  Player 2:
                </label>
                <input
                  type="text"
                  className="input-large"
                  name="player2"
                  id="player2"
                  value={player2}
                  onChange={(e) => setPlayer2(e.target.value)}
                  required
                />
                <br className="clear" />
                <label className="control-label" htmlFor="width">
                  Choose your board size:
                </label>
                <select
                  name="width"
                  value={width}
                  onChange={(e) => setWidth(e.target.value)}
                >
                  <option value="3">3 x 3</option>
                  <option value="4">4 x 4</option>
                  <option value="5">5 x 5</option>
                  <option value="6">6 x 6</option>
                </select>
                <br />
                <input
                  type="submit"
                  className="btn btn-info"
                  value="Start a new game"
                />
              </div>
            </fieldset>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Home;
