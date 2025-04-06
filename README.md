# 🍰 Sugar Rush: The Sweet Run

**Sugar Rush: The Sweet Run** is a fun, fast-paced 2D game built using Python's Pygame library. You play as a sugar-loving character trying to dodge healthy obstacles, collect sweets, and outrun the ever-persistent doctor! Choose wisely: too much sugar comes with consequences. 😅

---

## 🎮 Features

- **Single Player & Multiplayer Modes**  
  Compete alone or challenge a friend using different control keys.

- **Health & Sugar Mechanics**  
  Collect sweets for temporary boosts but beware of sugar crashes! Healthy foods like salad and vegetables help restore your health.

- **Doctor Chase Mechanic**  
  A doctor chases you down, adding pressure to make quick decisions and keep moving.

- **Dynamic Warnings**  
  High sugar consumption triggers on-screen warnings like "⚠️ Energy Running Low!"

- **Multiple Levels**  
  Time-limited levels (10s, 20s, 40s) with increasing difficulty.

- **Cool Countdown**  
  The game kicks off with a dynamic "3, 2, 1, GO!" countdown!

---

## 📚 Game Concepts Used

### 1. **Pygame**  
A Python library used for developing games with built-in support for handling graphics, sounds, and events.

### 2. **Player Movement**  
Control your character using arrow keys or WASD, allowing smooth navigation around the screen.

### 3. **Obstacles**  
Randomly spawned items like sweets and veggies affect your health and speed.

### 4. **Power-ups**  
- **High Sugar (🍰, 🍫, 🍦)**: Speed boost but drains health over time.  
- **Healthy Foods (🥗, 🥦)**: Restore health and give a balanced boost.

### 5. **Health Bar**  
Tracks your health. Reaching 0 results in Game Over.

### 6. **Sugar Rush Mechanic**  
Temporary speed boosts followed by a drop in performance—simulating a sugar crash.

### 7. **Game Over**  
Triggered if the doctor catches you or your health reaches 0.

### 8. **Event Handling**  
Keyboard and mouse inputs are used to move characters and interact with the UI.

---

## 🕹️ Controls

| Player      | Move Up | Move Down | Move Left | Move Right |
|-------------|---------|-----------|------------|-------------|
| Player 1    | ↑       | ↓         | ←          | →           |
| Player 2    | W       | S         | A          | D           |

---

## 🖼️ Assets

Ensure the following images are in the same directory as your Python script:
- `player.png`
- `doctor.png`
- `cake.png`
- `chocolate.png`
- `icecream.png`
- `salad.png`
- `vegetable.png`
- `background2.png`

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sugar-rush-game.git
cd sugar-rush-game
