# Go Fish — Rule-Based Expert System

A 2-player Go Fish game implemented in Python and Pygame-ce.

## Features

- Human vs AI
- Standard 52-card deck
- 7-card starting hand
- Books/sets of four
- Go Fish drawing
- Rule-based AI
- Knowledge base
- Inference engine
- AI decision explanation
- Keyboard restart with R
- New Game button

## Expert System Architecture

The AI is intentionally NOT based on machine learning.

### Knowledge Base
The expert system stores:
- AI's current cards
- Ranks previously requested by the human
- Ranks directly observed in the human's cards
- AI decision history

### Rule Base

1. If AI has 3 cards of a rank, prioritize completing the book.
2. If AI has 2 cards of a rank, prioritize the pair.
3. If the human previously requested a rank, increase its priority.
4. If the AI has direct evidence that the human has a rank, strongly prioritize it.
5. Use the number of matching AI cards as a secondary priority.
6. If no stronger rule applies, choose a legal rank deterministically.

### Inference Engine

For every AI turn:

Facts -> Rules -> Priority scores -> Highest-priority rank -> AI action

## Run

Install Python 3.10+.

Install the dependency:

    py -m pip install -r requirements.txt

Then run:

    py main.py

## Controls

- Click a rank button to ask the AI for that rank.
- R = New Game
- ESC = Quit

## Suggested Viva Explanation

"The project implements a production-rule expert system. The AI has a knowledge base containing its own hand and observations about the opponent. An inference engine evaluates explicit IF/THEN rules and assigns priorities to legal actions. The highest-priority action is selected as the AI's decision."

## Files

- main.py — application entry point
- cards.py — deck and card model
- player.py — player state and book detection
- game.py — Go Fish game engine
- expert_system.py — knowledge base, rules and inference engine
- ui.py — Pygame interface
