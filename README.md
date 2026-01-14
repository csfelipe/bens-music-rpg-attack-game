# Music RPG Attack Game

A music-themed RPG attack game built with Python and Pygame. Now available as a web version!

## How to Play

### Web Version (Easiest - No Installation Required!)

1. Simply open `index.html` in your web browser
2. Double-click the file or right-click and select "Open with" your preferred browser
3. The game will start automatically!

### Python Version (Original)

1. Install Python 3.7 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python main.py
   ```
   Or use the provided scripts:
   - Windows: `run_game.bat` or `run_game.ps1`
   - Mac/Linux: `python main.py`

## Game Features

- **Character Selection**: Choose from 7 different musical instruments (Flute, Clarinet, Saxophone, Trombone, Baritone, Tuba, and the unlockable Mafeoso)
- **Battle System**: Turn-based combat with three moves:
  - Normal Attack: Deal damage (lighter instruments can hit multiple times!)
  - Block: Reduce incoming damage by 70%
  - Super: Answer a music theory question for double damage
- **Difficulty Levels**: Easy, Medium, Hard, Expert, and Teacher Mode
- **Teacher Mode**: NPC learns your playstyle over 3 battles and adapts!
- **Achievements**: Unlock achievements by completing various challenges
- **Music Questions**: Test your knowledge of musical notes on a staff

## Controls

- **Arrow Keys**: Navigate menus and move selection
- **Enter/Space**: Select/Confirm
- **1/2/3**: Quick select moves in battle
- **ESC**: Cancel/Go back
- **Type letters**: Answer music questions (e.g., "C", "D", "E")

## Tips

- Lighter instruments (Flute, Clarinet) are faster and can hit multiple times, but have less HP and damage
- Heavier instruments (Tuba, Baritone) are slower but hit harder and have more HP
- Use Block strategically when you expect the NPC to attack
- Super moves are powerful but require answering music questions correctly
- Unlock Mafeoso by winning as Saxophone with less than 50% health remaining!
