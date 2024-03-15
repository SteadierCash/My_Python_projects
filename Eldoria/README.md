# Eldoria - Magic Quest

Welcome to Eldoria - Magic Quest! This console-based game takes you on an epic adventure through the mystical world of Eldoria, where magic reigns supreme and heroes are forged.

## Overview

Eldoria - Magic Quest is a text-based adventure game where you navigate through various paths, encounter enemies, cast powerful spells, wield enchanted weapons, and make critical decisions that shape your destiny.
## Game Files 
### Python files
- `main` - starts the game.
- `paths` = consists possible all possible paths that can be choosen during the game.

The game consist files containing different classes:

- `class_enemy`: Represents enemies encountered throughout the game.
- `class_game`: Manages the game's overall mechanics and flow.
- `class_hero`: Defines the player's character and attributes.
- `class_path`: Handles different paths and encounters in the game.
- `class_spell`: Manages spells and magical abilities.
- `class_weapon`: Handles weapons and combat mechanics.

### Json Files

The game utilizes several JSON files to store game data:

- `fight.json`: Contains data related to combat encounters.
- `friend.json`: Stores information about friendly characters and allies.
- `heroes.json`: Defines attributes and characteristics of heroes.
- `shop.json`: Lists items available for purchase in shops.
- `spell.json`: Holds data about magical spells and abilities.
- `story.json`: Provides narrative elements and plot points.
- `weapons.json`: Contains details about various weapons in the game.



## Classes

### *Weapon*

The `Weapon` class represents weapons that players can acquire in Eldoria - Magic Quest. 

#### Attributes

- `id`: An integer representing the unique identifier of the weapon.
- `name`: A string representing the name of the weapon.
- `power`: An integer representing the power level of the weapon. Higher power levels indicate stronger weapons.
- `strength`: An integer representing the strength level of the weapon. Higher strength levels indicate more durable weapons.

#### Methods
- `create_weapon()`: Generates a random weapon from the list of available weapons in the `weapons.json` file.
- `show_weapon()`: Returns a formatted string describing the weapon, including its name, power level, and strength level.
- `to_json()`: Returns a dictionary containing the attributes of the weapon in JSON format.

### *Spell*

The `Spell` class represents magical spells that players can cast in Eldoria - Magic Quest. 

#### Attributes

- `id`: An integer representing the unique identifier of the spell.
- `name`: A string representing the name of the spell.
- `power`: An integer representing the power increase of the spell. Higher power values indicate stronger spells.
- `strength`: An integer representing the strength increase of the spell. Higher strength values indicate more powerful spells.
- `heal`: An integer representing the healing effect of the spell. A positive value indicates the spell can heal the player.
- `kill`: An integer representing the killing effect of the spell. A positive value indicates the spell can instantly kill enemies.
- `disappear`: An integer representing the disappearing effect of the spell. A positive value indicates the spell allows the player to disappear and run from enemies.

#### Methods

- `create_spell()`: Generates a random spell from the list of available spells in the `spell.json` file.
- `show_spell()`: Returns a formatted string describing the spell, including its name and effects.
- `to_json()`: Returns a dictionary containing the attributes of the spell in JSON format.

### *Enemy*

The `Enemy` class represents an enemy that the player encounters during the game.

#### Attributes

- `name`: A string representing the name of the enemy.
- `power`: An integer representing the power of the enemy, calculated using the `stat` function based on the hero's power.
- `strength`: An integer representing the strength of the enemy, calculated using the `stat` function based on the hero's strength.
- `attack`: An integer representing the attack power of the enemy.
- `coins`: An integer representing the number of coins the enemy possesses, calculated based on its power or strength.

#### Methods

- `coins()`: Calculates the number of coins possessed by the enemy based on its power or strength.
- `__repr__()`: Returns a string representation of the enemy, including its name, power, strength, and defending coins.

#### Functions

- `stat(enemy, hero)`: Calculates the enemies strength/ power based on hero strength/power.
- `choose_enemy()`: Chooses enemy from **enemy.json** file. 

### *Hero*

The `Hero` class represents the player's character in Eldoria - Magic Quest. 

#### Attributes

- `name`: A string representing the name of the hero's character class.
- `power`: An integer representing the power attribute of the hero.
- `strength`: An integer representing the strength attribute of the hero.
- `lives`: An integer representing the current number of lives the hero has.
- `max_lives`: An integer representing the maximum number of lives the hero can have.
- `coins`: An integer representing the number of coins possessed by the hero.
- `attack`: An integer representing the attack power of the hero.
- `spells`: A list containing instances of the `Spell` class representing the spells possessed by the hero.
- `weapons`: A list containing instances of the `Weapon` class representing the weapons possessed by the hero.

#### Methods

- `show_hero_weapons()`: Returns a formatted string containing information about the weapons possessed by the hero.
- `show_hero_spells()`: Returns a formatted string containing information about the spells possessed by the hero.
- `choose_character(char_file)`: Selects a character for the hero from the specified JSON file.
- `__repr__()`: Returns a string representation of the hero, including its name, attributes, coins, spells, and weapons.

### *Game*

The `Game` class represents the main game mechanics and state in Eldoria - Magic Quest. It manages the player's interactions, including combat encounters, events, paths, and game progression.

#### Attributes

- `fight_outcome`: A string representing the outcome of a fight encounter.
- `hero`: An instance of the `Hero` class representing the player's character.
- `enemy`: An instance of the `Enemy` class representing the enemy encountered in combat.
- `event`: A string representing the current event or situation in the game.
- `path`: A string representing the current path or location in the game.
- `chapter`: An integer representing the current chapter or stage of the game.
- `strength_cost`: An integer representing the cost of increasing the hero's strength attribute.
- `power_cost`: An integer representing the cost of increasing the hero's power attribute.
- `lives_cost`: An integer representing the cost of purchasing additional lives for the hero.
- `weapons_cost`: An integer representing the cost of purchasing weapons in the game.
- `spells_cost`: An integer representing the cost of purchasing spells in the game.
- `chapter_1_decision`: A string representing the player's decision in chapter 1 of the game.


#### Methods
- `gameplay`: Main method to initiate and handle the gameplay.
- `save`: Saves the current game progress.
- `load`: Loads a previously saved game.
- `choose_hero`: Allows the player to select a hero for the game.
- `choose_path`: Provides options for the player to choose their path in the game.
- `what_action`: Allows the user to select an action from a choosen set (friend, shop, fight, story).
- `fight`: Manages combat between hero and choosen enemy.
- `outcome`: Determines the outcome of a fight.
- `attack`: Handles the hero's attacks during combat.
- `use_weapon`: Allows the hero to use a weapon during combat.
- `use_spell`: Enables the hero to use spells during combat.
- `run`: Provides the option for the hero to flee from combat. There is a 1/5 chance that the hero will lose 2 lives when attempting to flee.
- `upgrade_attribute`: Function used to upgrade attributes during shopping.
- `shop`: Allows the hero to purchase items or upgrades.
- `friend`: Provides bonuses to the hero based on chosen friends.
- `story`: Manages the game's storyline.
- `chapter_0` to `chapter_5`: Different chapters of the game's story.
- `death`: Handles the player's death scenario.
- `print_chapter`: Formats a string indicating the current chapter the player is in.


## Usage

To play Eldoria - Magic Quest:

1. Ensure you have a compatible environment to run Python scripts.
2. Download the game files and JSON data files.
3. Run the main game script (`main.py`) using Python.
4. Follow the prompts and instructions displayed in the console to navigate through the game, make choices, and progress through the story.



Enjoy your adventure in Eldoria - Magic Quest! May your magic be strong and your courage unwavering as you journey through the realm of mystery and enchantment.
