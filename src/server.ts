/**
 * Express server for Tritina game
 */
import express, { Request, Response } from "express";
import cors from "cors";
import path from "path";
import { Board, Player } from "./game";
import { GameDatabase } from "./database";

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Initialize database
const db = new GameDatabase();

// Serve static files from client build in production
if (process.env.NODE_ENV === "production") {
  app.use(express.static(path.join(__dirname, "../client/build")));
}

// API Routes

/**
 * Create a new game
 */
app.post("/api/game", (req: Request, res: Response) => {
  try {
    const { player1, player2, width } = req.body;

    if (!player1 || !player2 || !width) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const players = [new Player(player1), new Player(player2)];
    const board = new Board(players, parseInt(width), parseInt(width));
    const boardId = db.insertGame(board);

    res.json({ boardId, board });
  } catch (error) {
    console.error("Error creating game:", error);
    res.status(500).json({ error: "Failed to create game" });
  }
});

/**
 * Get game state
 */
app.get("/api/game/:id", (req: Request, res: Response) => {
  try {
    const boardId = parseInt(req.params.id);
    const board = db.getGame(boardId);

    if (!board) {
      return res.status(404).json({ error: "Game not found" });
    }

    res.json({ board, id: boardId });
  } catch (error) {
    console.error("Error getting game:", error);
    res.status(500).json({ error: "Failed to get game" });
  }
});

/**
 * Play a tile
 */
app.post("/api/play", (req: Request, res: Response) => {
  try {
    const { board_id, tile } = req.body;

    if (board_id === undefined || tile === undefined) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const boardId = parseInt(board_id);
    const tileNum = parseInt(tile);
    const board = db.getGame(boardId);

    if (!board) {
      return res.status(404).json({ error: "Game not found" });
    }

    const played = board.playTile(
      tileNum,
      board.players[board.turn % board.players.length]
    );
    board.turn += 1;

    if (played) {
      db.updateGame(boardId, board);
      res.json(board);
    } else {
      res.status(400).json({ error: "Invalid move" });
    }
  } catch (error) {
    console.error("Error playing tile:", error);
    res.status(500).json({ error: "Failed to play tile" });
  }
});

/**
 * Poll for game updates
 */
app.post("/api/poll", (req: Request, res: Response) => {
  try {
    const { board_id } = req.body;

    if (board_id === undefined) {
      return res.status(400).json({ error: "Missing board_id" });
    }

    const boardId = parseInt(board_id);
    const board = db.getGame(boardId);

    if (!board) {
      return res.status(404).json({ error: "Game not found" });
    }

    res.json(board);
  } catch (error) {
    console.error("Error polling game:", error);
    res.status(500).json({ error: "Failed to poll game" });
  }
});

// Serve React app for all other routes in production
if (process.env.NODE_ENV === "production") {
  app.get("*", (req: Request, res: Response) => {
    res.sendFile(path.join(__dirname, "../client/build/index.html"));
  });
}

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

// Handle shutdown
process.on("SIGINT", () => {
  db.close();
  process.exit(0);
});
