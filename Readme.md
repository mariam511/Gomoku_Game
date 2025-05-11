# Gomoku (Five in a Row) Game Solver 🎮

## 📌 Project Overview

**Gomoku** is a strategy board game where players compete to get **five of their marks in a row** — either **horizontally, vertically, or diagonally** — on a game board. This project implements a **Gomoku game solver** in Python with both **Human vs AI** and **AI vs AI** modes.

### 🎯 Game Modes

- **Human vs AI**  
  Play against an AI that uses the **Minimax algorithm** to make optimal moves.

- **AI vs AI**  
  Watch two AIs compete — one using **Minimax**, the other using **Alpha-Beta Pruning**.

---

## 🧱 Project Components

### 🧠 Game Engine
- Handles move validation, rule enforcement, and win/draw conditions.
- Uses depth-limited **Minimax** and **Alpha-Beta Pruning** algorithms for move selection.

### 📋 Input
- Users specify:
  - **Board size**: 15x15 or 19x19
  - **Player symbol**: B (Black) or W (White)
  - **Current game state**, or start a new one

### 🖥️ Output
- The board state is rendered in the console after each move.
- AI outputs its chosen move coordinates.

---

## 🧠 Algorithms Implemented

### ✅ Minimax Algorithm
- Explores all possible moves up to a specified depth.
- Evaluates each move recursively to choose the optimal one for the current player.

### ✅ Alpha-Beta Pruning
- An optimization of Minimax that prunes branches that won’t affect the final decision.
- Speeds up computation without sacrificing decision quality.
