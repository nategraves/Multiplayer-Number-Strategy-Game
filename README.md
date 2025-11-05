# Multiplayer Number Strategy Game (Tritina)

A multiplayer number strategy game built with Node.js, Express, React, and TypeScript.

## Installation

### Backend Dependencies
```bash
npm install
```

### Frontend Dependencies
```bash
cd client
npm install
```

## Running the Application

### Development Mode

Start the backend server:
```bash
npm run dev
```

In a separate terminal, start the React frontend:
```bash
npm run client
```

The server runs on `http://localhost:5000` and the React app on `http://localhost:3000`.

### Production Mode

Build both backend and frontend:
```bash
npm run build
```

Start the server:
```bash
NODE_ENV=production npm start
```

## How to Play

1. Navigate to the home page
2. Enter player names and select board size
3. Take turns clicking on tiles with value "0"
4. Match 3 or more adjacent tiles to score points
5. The tile values increment and matched tiles reset

## Technology Stack

- **Backend**: Node.js, Express, TypeScript, better-sqlite3
- **Frontend**: React, TypeScript, React Router
- **Database**: SQLite

