# Music RPG Attack Game

A music-themed RPG battle game where you fight as musical instruments! Choose your character, battle opponents, and test your music theory knowledge with Super moves.

## 🎮 How to Play

### Web Version (Recommended - No Installation Required!)

1. Simply open `index.html` in your web browser
2. Double-click the file or right-click and select "Open with" your preferred browser
3. The game will start automatically!

**No installation, no dependencies - just open and play!**

### Python Version (Original)

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```
   Or use the provided scripts:
   - Windows: `run_game.bat` or `run_game.ps1`
   - Mac/Linux: `python main.py`

## 🎵 Game Features

### Characters
Choose from **7 different musical instruments**, each with unique stats:
- **Flute**: Fastest speed, lowest weight (low HP, low damage) - Can hit 2-3 times!
- **Clarinet**: Fast speed, low weight (low-medium HP, low-medium damage)
- **Saxophone**: Medium speed, medium weight (medium HP, medium damage)
- **Trombone**: Slow speed, high weight (high HP, high damage)
- **Baritone**: Very slow speed, very high weight (very high HP, very high damage)
- **Tuba**: Slowest speed, highest weight (highest HP, highest damage)
- **Mafeoso**: Unlockable character (high HP and damage, mysterious character)

### Battle System
Turn-based combat with **three strategic moves**:
- **Normal Attack**: Deal damage based on your instrument's base damage
  - Lighter instruments (weight 1-2) can hit **2-3 times** per attack!
  - Medium instruments (weight 3-4) can hit **1-2 times**
  - Heavy instruments (weight 5+) hit **once** but deal massive damage
- **Block**: Prepare to defend - reduces incoming damage by 70%
- **Super**: Answer a music theory question correctly for **double damage**!

### Difficulty Levels
- **Easy**: NPC is slower and less accurate
- **Medium**: Balanced challenge
- **Hard**: NPC is faster and more strategic
- **Expert**: NPC is very fast and highly accurate
- **Teacher Mode**: Special mode where NPC learns your playstyle over 3 battles
  - NPC **never attacks** - you can practice freely!
  - NPC adapts and counters your strategies in future battles

### Achievements
Unlock achievements by completing challenges:
- **Win**: Win a game
- **Now you have to pay your taxes**: Lose a game
- **Why**: Win as any character
- **That the tune i love**: Win as Saxophone with under 50% health (unlocks Mafeoso!)
- **It bird it a plane what nooooooo**: Win without using super moves

### Music Theory Questions
Test your knowledge during Super moves:
- Identify notes on a musical staff
- Questions adapt to your instrument's clef (treble or bass)
- Answer correctly for massive damage!

## ⌨️ Controls

### Menu Navigation
- **Arrow Keys**: Navigate through options
- **Enter/Space**: Select/Confirm
- **ESC**: Go back (works on all select screens)

### Battle Controls
- **SPACE or ENTER**: Open move selection menu
- **Arrow Keys**: Navigate moves in the menu
- **1/2/3**: Quick select moves (1=Attack, 2=Block, 3=Super)
- **Enter**: Confirm selected move
- **ESC**: Cancel move selection
- **Type letters**: Answer music questions (e.g., "C", "D", "E", "F#")

### Mouse Controls
- Click on character cards to select
- Click on moves in the battle menu to select
- Click "Select Move" button to open move menu

## 💡 Tips & Strategy

### Character Selection
- **Lighter instruments** (Flute, Clarinet): Fast and can hit multiple times, but fragile
- **Heavier instruments** (Tuba, Baritone): Slow but tanky with high damage
- **Medium instruments** (Saxophone, Trombone): Balanced stats

### Battle Tips
- Use **Block** strategically when you expect the NPC to attack
- **Super moves** are powerful but risky - make sure you know your music theory!
- Lighter instruments benefit from multiple hits - great for wearing down enemies
- Heavier instruments deal massive single hits - perfect for finishing moves
- In **Teacher Mode**, practice your moves freely - the NPC won't attack!

### Unlocking Mafeoso
Win a battle as **Saxophone** while having **less than 50% health** remaining. This unlocks the powerful Mafeoso character!

## 🎯 Game Flow

1. **Title Screen**: View countdown timer and select "Start" or "Achievements"
2. **Character Select**: Choose your instrument (use arrow keys or click)
3. **NPC Select**: Choose your opponent
4. **Difficulty Select**: Choose difficulty level or Teacher Mode
5. **Battle**: Fight using your moves!
6. **Results**: Win or lose, then return to character select

## 🛠️ Technical Details

- **Web Version**: Pure HTML, CSS, and JavaScript - no frameworks required
- **Python Version**: Built with Pygame
- **Browser Compatibility**: Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- **No Internet Required**: Play offline once files are downloaded

## 📝 Notes

- The game features a countdown timer on the title screen
- Teacher Mode allows you to practice without NPC attacks
- All character sprites are procedurally generated
- Music questions use standard musical notation

## 🎉 Have Fun!

Enjoy battling with musical instruments and testing your music theory knowledge!
