/**
 * Game logic for the Tritina multiplayer number strategy game
 */

function uniqify<T>(seq: T[]): T[] {
  const seen = new Set<T>();
  return seq.filter((x) => {
    if (seen.has(x)) {
      return false;
    }
    seen.add(x);
    return true;
  });
}

export interface Tile {
  value: number;
  graph: number[];
}

export class Player {
  name: string;
  score: number;

  constructor(name?: string) {
    this.score = 0;
    this.name = name || "Player";
  }
}

export class Board {
  players: Player[];
  width: number;
  height: number;
  totalTiles: number;
  turn: number;
  lastPlayed: number | null;
  tiles: Tile[];

  constructor(players?: Player[], width: number = 3, height: number = 3) {
    if (players) {
      this.players = players;
    } else {
      this.players = [new Player("Player 1"), new Player("Player 2")];
    }

    this.width = parseInt(width.toString());
    this.height = parseInt(height.toString());
    this.totalTiles = this.width * this.height;
    this.turn = 0;
    this.lastPlayed = null;
    this.tiles = [];

    // Initialize tiles with their adjacency graph
    for (let i = 0; i < this.totalTiles; i++) {
      const graph: number[] = [];

      // Current tile isn't in the leftmost column
      if (i % this.width !== 0) {
        // Add the tile to the left
        graph.push(i - 1);
      }

      // Current tile isn't in the rightmost column
      if (i % this.width !== this.width - 1) {
        // Add the tile to the right
        graph.push(i + 1);
      }

      // Current tile isn't in first row
      if (i >= this.width) {
        // Add the tile above
        graph.push(i - this.width);
      }

      // Current tile isn't in the last row
      if (i < this.totalTiles - this.width) {
        // Add the tile below
        graph.push(i + this.width);
      }

      // Append the graph and initial value
      this.tiles.push({
        value: 0,
        graph: graph,
      });
    }
  }

  playTile(
    tile: number,
    player: Player,
    increment: boolean = false,
    timeThrough: number = 1
  ): boolean {
    if (timeThrough === 1) {
      this.lastPlayed = tile;
      this.increment(tile);
    }
    const nodes = this.getNodes(tile, [], true);

    if (nodes.length > 2) {
      this.players[this.turn % 2].score +=
        nodes.length * this.getValue(nodes[0]);
      for (let i = 0; i < nodes.length; i++) {
        if (i === 0) {
          this.increment(nodes[i]);
          timeThrough = 1;
        } else {
          this.setValue(nodes[i], 0);
        }
      }
      timeThrough += 1;
      this.playTile(nodes[0], player, true, timeThrough);
    }
    return true;
  }

  getNodes(current: number, nodes: number[], first: boolean): number[] {
    nodes = nodes.concat([current]);

    const graph = this.tiles[current].graph;

    for (const each of graph) {
      if (!nodes.includes(each)) {
        if (this.getValue(each) === this.getValue(current)) {
          const newpath = this.getNodes(each, nodes, false);
          if (newpath) {
            nodes = nodes.concat(newpath);
          }
        }
      }
    }
    nodes = uniqify(nodes);
    return nodes;
  }

  increment(tile: number): void {
    this.tiles[tile].value += 1;
  }

  getValue(tile: number): number {
    return this.tiles[tile].value;
  }

  setValue(tile: number, value: number): void {
    this.tiles[tile].value = value;
  }

  serialize(): string {
    const players = this.players.map((each) => ({
      name: each.name,
      score: each.score,
    }));
    return JSON.stringify({
      players: players,
      tiles: this.tiles,
      turn: this.turn,
    });
  }
}
