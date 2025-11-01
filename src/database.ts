/**
 * Database module for handling game persistence
 */
import Database from "better-sqlite3";
import { Board, Player } from "./game";

const DB_PATH = "./tritina.db";

export class GameDatabase {
  private db: Database.Database;

  constructor(dbPath: string = DB_PATH) {
    this.db = new Database(dbPath);
    this.initDb();
  }

  initDb(): void {
    const sql = `
      DROP TABLE IF EXISTS games;
      CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        board TEXT NOT NULL
      );
    `;
    this.db.exec(sql);
  }

  insertGame(board: Board): number {
    const jsonBoard = JSON.stringify(board);
    const stmt = this.db.prepare("INSERT INTO games (board) VALUES (?)");
    const result = stmt.run(jsonBoard);
    return result.lastInsertRowid as number;
  }

  getGame(id: number): Board | null {
    const stmt = this.db.prepare("SELECT * FROM games WHERE id = ?");
    const row = stmt.get(id) as { id: number; board: string } | undefined;

    if (!row) {
      return null;
    }

    // Deserialize the board
    const data = JSON.parse(row.board);
    const players = data.players.map(
      (p: { name: string; score: number }) => {
        const player = new Player(p.name);
        player.score = p.score;
        return player;
      }
    );
    const board = new Board(players, data.width, data.height);
    board.tiles = data.tiles;
    board.turn = data.turn;
    board.lastPlayed = data.lastPlayed;
    return board;
  }

  updateGame(id: number, board: Board): void {
    const jsonBoard = JSON.stringify(board);
    const stmt = this.db.prepare("UPDATE games SET board = ? WHERE id = ?");
    stmt.run(jsonBoard, id);
  }

  close(): void {
    this.db.close();
  }
}
