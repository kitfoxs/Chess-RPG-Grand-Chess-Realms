import os
import time
import random
import pickle
import chess
import chess.engine

class ChessRPG:
    def __init__(self):
        # Game state
        self.player = {
            "name": "",
            "background": "",
            "alignment": "neutral",  # Can be white, black, or neutral
            "inventory": [],
            "quests": [],
            "visited_locations": [],
            "chess_wins": 0,
            "chess_losses": 0,
            "chess_draws": 0
        }
        
        # Game world
        self.current_location = None
        self.locations = {}
        self.npcs = {}
        
        # Chess engine setup
        try:
            # Update the path to your stockfish executable
            self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
            print("Chess engine loaded successfully.")
        except:
            print("Warning: Stockfish chess engine not found. Please install it for chess battles.")
            self.engine = None
        
        # Game flags
        self.game_running = True
        
        # Initialize game components
        self.load_world()
    
    def load_world(self):
        """Load all locations, NPCs, and quests"""
        # Initialize starter locations
        self.locations = {
            "white_village": {
                "name": "The White Village",
                "description": "A small, peaceful village under the protection of the White Kingdom. Cottages with thatched roofs surround a central square where villagers gather to trade and play chess on stone tables.",
                "exits": {"north": "town_square", "east": "village_outskirts", "west": "forest_path"},
                "npcs": ["elder_thomas", "innkeeper_clara"],
                "items": ["basic_chess_set"],
                "visited": False
            },
            "town_square": {
                "name": "Town Square",
                "description": "The heart of the White Village. A large chessboard is inlaid in the cobblestone center where local tournaments are held. The Elder's house stands prominently to the north.",
                "exits": {"south": "white_village", "north": "elders_house"},
                "npcs": ["village_champion"],
                "items": [],
                "visited": False
            },
            "elders_house": {
                "name": "Elder's House",
                "description": "A modest but well-kept home with bookshelves lining the walls. A beautiful ivory chess set sits on a table by the window, the pieces catching the light.",
                "exits": {"south": "town_square"},
                "npcs": ["elder_thomas"],
                "items": ["lore_book_white_kingdom"],
                "visited": False
            },
            "village_outskirts": {
                "name": "Village Outskirts",
                "description": "The houses become fewer as the village gives way to rolling farmland. A weathered signpost points to various destinations.",
                "exits": {"west": "white_village", "east": "crossroads"},
                "npcs": ["traveling_merchant"],
                "items": [],
                "visited": False
            },
            "forest_path": {
                "name": "Forest Path",
                "description": "A winding path through ancient oaks. Dappled sunlight filters through the leaves, creating a pattern reminiscent of a chessboard on the forest floor.",
                "exits": {"east": "white_village", "north": "hermits_clearing"},
                "npcs": [],
                "items": ["mysterious_scroll"],
                "visited": False
            },
            "hermits_clearing": {
                "name": "Hermit's Clearing",
                "description": "A small, peaceful clearing with a humble hut. Outside stands a stone table with a chessboard carved into its surface. The pieces are made of polished wood, worn from years of use.",
                "exits": {"south": "forest_path"},
                "npcs": ["hermit_sage"],
                "items": [],
                "visited": False
            },
            "crossroads": {
                "name": "The Crossroads",
                "description": "A junction where several paths meet. A weathered stone marker indicates directions to different kingdoms. The path to the east grows darker, suggesting the border of the Black Kingdom lies that way.",
                "exits": {"west": "village_outskirts", "east": "checkered_frontier", "north": "highland_road"},
                "npcs": ["wandering_knight"],
                "items": [],
                "visited": False
            }
        }
        
        # Initialize starter NPCs
        self.npcs = {
            "elder_thomas": {
                "name": "Elder Thomas",
                "description": "A wise old man with a long white beard and kind eyes. He has governed the White Village for decades.",
                "dialogue": {
                    "greeting": "Welcome, traveler. Our village may be small, but we pride ourselves on our strategic minds.",
                    "white_kingdom": "The White Kingdom has protected us for generations. They value honor and tradition above all.",
                    "chess": "Chess is more than a game here—it's how we resolve conflicts and teach our young to think ahead.",
                    "quest": "Our village has been troubled by a rogue chess player who challenges locals and takes their prized possessions when they lose. Would you confront him on our behalf?"
                },
                "chess_skill": 1200,  # Elo rating
                "quest": "defeat_village_champion"
            },
            "innkeeper_clara": {
                "name": "Innkeeper Clara",
                "description": "A plump, cheerful woman who runs the local inn. She's known for her hospitality and her surprisingly sharp chess skills.",
                "dialogue": {
                    "greeting": "Welcome to the White Rook Inn! Care for a game while your meal is prepared?",
                    "rumors": "They say the Hermit in the forest was once the White Kingdom's champion before he gave it all up.",
                    "black_kingdom": "I've heard their inns serve wine in chalices shaped like chess pieces. Fancy, but impractical if you ask me!"
                },
                "chess_skill": 1000,
                "quest": None
            },
            "village_champion": {
                "name": "Rowan the Black Bandit",
                "description": "A confident young man in dark clothing, with a smirk that suggests he rarely loses. A fine chess set hangs at his belt, with pieces made from the winnings of previous matches.",
                "dialogue": {
                    "greeting": "Another challenger? How dull. None in this village can match my skill.",
                    "challenge": "If you wish to play, we must make it interesting. Your finest possession against mine."
                },
                "chess_skill": 1400,
                "quest": "defeat_village_champion",
                "hostile": True
            },
            "hermit_sage": {
                "name": "Elowen the Hermit of the 8th Rank",
                "description": "An elderly figure with piercing eyes that seem to see beyond the physical. Her hut is decorated with chess symbols and old scrolls.",
                "dialogue": {
                    "greeting": "Few find their way to my clearing. Are you lost, or seeking?",
                    "wisdom": "The board has 64 squares, just as life has many paths. Choose wisely which you step upon.",
                    "training": "I could teach you a few moves I've developed over the years. But first, you must prove your worth with a game."
                },
                "chess_skill": 1600,
                "quest": "hermit_training"
            },
            "wandering_knight": {
                "name": "Sir Galwynne",
                "description": "A knight in weathered armor bearing neither White nor Black insignia. A gray chess knight is emblazoned on his tunic.",
                "dialogue": {
                    "greeting": "Hail, traveler. May your path be clear and your strategies sound.",
                    "neutral": "I serve neither kingdom now. I follow only the codes of honorable play.",
                    "conflict": "When disputes arise, I offer my board as neutral ground. Chess resolves what swords would only make worse."
                },
                "chess_skill": 1500,
                "quest": "knight_challenge"
            }
        }
        
        # Set starting location
        self.current_location = self.locations["white_village"]
    
    def start_game(self):
        """Initialize and begin the game"""
        self.display_welcome()
        self.create_character()
        
        # Main game loop
        while self.game_running:
            self.display_location()
            command = input("\n> ").strip().lower()
            self.process_command(command)
    
    def display_welcome(self):
        """Show the game's welcome message and introduction"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 80)
        print(" " * 25 + "THE GRAND CHESS REALMS" + " " * 25)
        print("=" * 80)
        print("\nWelcome to a world where chess is more than a game—it's the language of power,")
        print("diplomacy, and conflict. From humble village disputes to the clash of kingdoms,")
        print("every significant challenge is resolved on the checkered board.")
        print("\nIn this land divided between the honorable White Kingdom and the cunning Black Kingdom,")
        print("your strategic mind will be your greatest weapon.")
        print("\n" + "=" * 80)
        input("\nPress Enter to begin your journey...")
    
    def create_character(self):
        """Handle character creation process"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("CHARACTER CREATION")
        print("=================\n")
        
        self.player["name"] = input("What is your name, traveler? ").strip()
        
        print("\nChoose your background:")
        backgrounds = [
            "Knight (Warrior devoted to honor and battle strategy)",
            "Rogue (Cunning trickster skilled in deception)",
            "Mage (Master of arcane knowledge who sees chess as a gateway to power)",
            "Noble Strategist (Political mastermind leveraging strategy)",
            "Wandering Philosopher (Seeker of knowledge and enlightenment)"
        ]
        
        for i, bg in enumerate(backgrounds, 1):
            print(f"{i}. {bg}")
        
        choice = 0
        while choice < 1 or choice > len(backgrounds):
            try:
                choice = int(input("\nSelect a number: "))
            except:
                pass
        
        # Extract just the class name (before the parenthesis)
        self.player["background"] = backgrounds[choice-1].split(" (")[0]
        
        print(f"\nWelcome, {self.player['name']} the {self.player['background']}!")
        print("Your journey in the Grand Chess Realms begins in a small village under")
        print("the protection of the White Kingdom.")
        input("\nPress Enter to continue...")
    
    def display_location(self):
        """Show the current location description and available options"""
        os.system('cls' if os.name == 'nt' else 'clear')
        location = self.current_location
        
        # Mark as visited
        if not location["visited"]:
            location["visited"] = True
            self.player["visited_locations"].append(location["name"])
        
        # Display location header
        print("=" * 80)
        print(f" {location['name'].upper()}")
        print("=" * 80)
        
        # Display description
        print(f"\n{location['description']}")
        
        # Show available exits
        print("\nExits:")
        for direction, destination in location["exits"].items():
            dest_name = self.locations[destination]["name"]
            print(f"  {direction.capitalize()} - {dest_name}")
        
        # Show NPCs present
        if location["npcs"]:
            print("\nPeople:")
            for npc_id in location["npcs"]:
                if npc_id in self.npcs:  # Make sure NPC exists
                    print(f"  {self.npcs[npc_id]['name']}")
        
        # Show items present
        if location["items"]:
            print("\nItems:")
            for item in location["items"]:
                print(f"  {item.replace('_', ' ').title()}")
        
        # Show commands
        print("\nCommands: MOVE [direction], TALK TO [person], EXAMINE [item/person],")
        print("          TAKE [item], INVENTORY, QUIT, HELP")
    
    def process_command(self, command):
        """Parse and execute the player's command"""
        # Split the command into words
        words = command.split()
        
        if not words:
            return
        
        action = words[0]
        
        # Handle movement commands
        if action in ["move", "go", "travel"]:
            if len(words) > 1:
                self.move_player(words[1])
            else:
                print("Move where? Please specify a direction.")
                input("Press Enter to continue...")
        
        # Handle talking to NPCs
        elif action == "talk" and len(words) > 1 and words[1] == "to":
            if len(words) > 2:
                self.talk_to_npc(" ".join(words[2:]))
            else:
                print("Talk to whom? Please specify a person.")
                input("Press Enter to continue...")
        
        # Handle examining
        elif action in ["examine", "look", "inspect"]:
            if len(words) > 1:
                self.examine_target(" ".join(words[1:]))
            else:
                print("Examine what? Please specify a target.")
                input("Press Enter to continue...")
        
        # Handle taking items
        elif action in ["take", "get", "pickup"]:
            if len(words) > 1:
                self.take_item(" ".join(words[1:]))
            else:
                print("Take what? Please specify an item.")
                input("Press Enter to continue...")
        
        # Handle inventory
        elif action == "inventory":
            self.show_inventory()
        
        # Handle challenge
        elif action == "challenge":
            if len(words) > 1:
                self.challenge_to_chess(" ".join(words[1:]))
            else:
                print("Challenge whom? Please specify a person.")
                input("Press Enter to continue...")
        
        # Handle help
        elif action == "help":
            self.show_help()
        
        # Handle quitting
        elif action in ["quit", "exit"]:
            confirm = input("Are you sure you want to quit? (y/n): ").lower()
            if confirm.startswith("y"):
                self.game_running = False
        
        else:
            print("I don't understand that command.")
            input("Press Enter to continue...")
    
    def move_player(self, direction):
        """Move the player in the specified direction"""
        direction = direction.lower()
        
        if direction in self.current_location["exits"]:
            destination = self.current_location["exits"][direction]
            self.current_location = self.locations[destination]
        else:
            print(f"You cannot go {direction} from here.")
            input("Press Enter to continue...")
    
    def talk_to_npc(self, npc_name):
        """Handle conversation with an NPC"""
        # Find the NPC in the current location
        npc_id = None
        for npc in self.current_location["npcs"]:
            if npc_name.lower() in self.npcs[npc]["name"].lower():
                npc_id = npc
                break
        
        if not npc_id:
            print(f"There's no one named {npc_name} here.")
            input("Press Enter to continue...")
            return
        
        npc = self.npcs[npc_id]
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== Conversation with {npc['name']} ===\n")
        print(f"{npc['name']}: \"{npc['dialogue']['greeting']}\"")
        
        # Continue conversation until player exits
        talking = True
        while talking:
            print("\nTopics:")
            topics = [topic for topic in npc["dialogue"].keys() if topic != "greeting"]
            for i, topic in enumerate(topics, 1):
                print(f"{i}. Ask about {topic.replace('_', ' ').title()}")
            print(f"{len(topics) + 1}. End conversation")
            
            if npc.get("quest") and not npc.get("hostile", False):
                print(f"{len(topics) + 2}. Accept quest")
            
            if not npc.get("hostile", False):
                print(f"{len(topics) + 3}. Challenge to chess")
            
            choice = 0
            while choice < 1 or choice > len(topics) + 3:
                try:
                    choice = int(input("\nSelect a number: "))
                except:
                    pass
            
            if choice <= len(topics):
                topic = topics[choice - 1]
                print(f"\n{self.player['name']}: Tell me about {topic.replace('_', ' ')}.")
                print(f"{npc['name']}: \"{npc['dialogue'][topic]}\"")
                input("\nPress Enter to continue...")
            
            elif choice == len(topics) + 1:
                talking = False
            
            elif choice == len(topics) + 2 and npc.get("quest"):
                print(f"\n{self.player['name']}: I'll help you with this task.")
                if npc["quest"] not in self.player["quests"]:
                    self.player["quests"].append(npc["quest"])
                    print(f"Quest accepted: {npc['quest'].replace('_', ' ').title()}")
                else:
                    print("You've already accepted this quest.")
                input("\nPress Enter to continue...")
            
            elif choice == len(topics) + 3 and not npc.get("hostile", False):
                self.challenge_to_chess(npc["name"])
                talking = False
    
    def examine_target(self, target):
        """Examine an NPC or item in the current location"""
        # Check if target is an NPC
        for npc_id in self.current_location["npcs"]:
            if target.lower() in self.npcs[npc_id]["name"].lower():
                print(f"\n{self.npcs[npc_id]['description']}")
                input("\nPress Enter to continue...")
                return
        
        # Check if target is an item
        for item in self.current_location["items"]:
            if target.lower() in item.lower():
                # Simple item descriptions for now
                descriptions = {
                    "basic_chess_set": "A simple wooden chess set with hand-carved pieces. It's well-used but still in good condition.",
                    "lore_book_white_kingdom": "A leather-bound tome titled 'Chronicles of the White Kingdom.' It contains histories and myths of Albion.",
                    "mysterious_scroll": "A weathered scroll sealed with a wax emblem showing a chess piece. The seal remains unbroken."
                }
                
                if item in descriptions:
                    print(f"\n{descriptions[item]}")
                else:
                    print(f"\nA {item.replace('_', ' ')}. Nothing particularly notable about it.")
                
                input("\nPress Enter to continue...")
                return
        
        print(f"You don't see {target} here.")
        input("Press Enter to continue...")
    
    def take_item(self, item_name):
        """Take an item from the current location"""
        for item in self.current_location["items"]:
            if item_name.lower() in item.lower():
                self.player["inventory"].append(item)
                self.current_location["items"].remove(item)
                print(f"You took the {item.replace('_', ' ')}.")
                input("Press Enter to continue...")
                return
        
        print(f"There's no {item_name} here to take.")
        input("Press Enter to continue...")
    
    def show_inventory(self):
        """Display the player's inventory"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== INVENTORY ===\n")
        
        if not self.player["inventory"]:
            print("Your inventory is empty.")
        else:
            for item in self.player["inventory"]:
                print(f"- {item.replace('_', ' ').title()}")
        
        input("\nPress Enter to continue...")
    
    def challenge_to_chess(self, npc_name):
        """Challenge an NPC to a chess match"""
        # Find the NPC
        npc_id = None
        for npc in self.current_location["npcs"]:
            if npc_name.lower() in self.npcs[npc]["name"].lower():
                npc_id = npc
                break
        
        if not npc_id:
            print(f"There's no one named {npc_name} here to challenge.")
            input("Press Enter to continue...")
            return
        
        npc = self.npcs[npc_id]
        
        # Chess match setup
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== CHESS CHALLENGE: {self.player['name']} vs. {npc['name']} ===\n")
        
        # Narrative introduction to the match
        print(f"{npc['name']} accepts your challenge.")
        print("As you both take your places at the board, a sense of anticipation fills the air.")
        print(f"The {npc['name'].split()[0]} will play as Black, you will play as White.")
        
        if npc.get("hostile", False):
            print(f"\n{npc['name']}: \"You'll regret challenging me, {self.player['name']}. Your defeat is inevitable.\"")
        else:
            print(f"\n{npc['name']}: \"May the best strategist win.\"")
        
        input("\nPress Enter to begin the match...")
        
        # If we have a chess engine, play a real game
        if self.engine:
            result = self.play_chess_match(npc["chess_skill"])
            
            # Handle the result
            self.handle_chess_result(result, npc)
        else:
            # No chess engine, simulate the match
            print("\nNo chess engine found. The match will be simulated.")
            time.sleep(2)
            
            # Simple probability-based outcome based on skill difference
            player_skill = 1200  # Default player skill
            skill_diff = player_skill - npc["chess_skill"]
            win_chance = 0.5 + (skill_diff / 1000)  # Adjust probability based on skill
            win_chance = max(0.1, min(0.9, win_chance))  # Cap between 10% and 90%
            
            result = random.random()
            if result < win_chance:
                self.handle_chess_result("win", npc)
            elif result < win_chance + 0.2:  # 20% chance of draw
                self.handle_chess_result("draw", npc)
            else:
                self.handle_chess_result("loss", npc)
    
    def play_chess_match(self, opponent_elo):
        """Play an actual chess match against the engine"""
        board = chess.Board()
        
        # Set up the chess engine with appropriate Elo level
        self.engine.configure({"Skill Level": self.elo_to_skill_level(opponent_elo)})
        
        # Main chess loop
        while not board.is_game_over():
            # Display the board
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.render_board(board))
            
            if board.turn == chess.WHITE:  # Player's turn
                print("\nYour turn (White)")
                move_uci = input("Enter move in UCI format (e.g., e2e4, g1f3): ").strip()
                
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        board.push(move)
                    else:
                        print("Illegal move. Try again.")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid format. Please use UCI notation (e.g., e2e4).")
                    input("Press Enter to continue...")
            
            else:  # Engine's turn
                print("\nOpponent is thinking...")
                result = self.engine.play(board, chess.engine.Limit(time=1.0))
                board.push(result.move)
                print(f"Opponent played: {result.move.uci()}")
                time.sleep(1)
        
        # Display final board state
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.render_board(board))
        
        # Determine the result
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return "loss"
            else:
                return "win"
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_fifty_moves():
            return "draw"
        else:
            return "draw"  # Default case
    
    def render_board(self, board):
        """Render the chess board in ASCII"""
        board_str = str(board)
        
        # Convert to cleaner ASCII representation
        rows = board_str.split('\n')
        output = []
        
        output.append("  a b c d e f g h")
        output.append(" +-----------------+")
        
        for i, row in enumerate(rows):
            output.append(f"{8-i}| {' '.join(row)} |")
        
        output.append(" +-----------------+")
        output.append("  a b c d e f g h")
        
        return '\n'.join(output)
    
    def elo_to_skill_level(self, elo):
        """Convert Elo rating to Stockfish skill level (0-20)"""
        # Simple mapping of Elo ranges to skill levels
        if elo < 800:
            return 0
        elif elo < 1000:
            return 3
        elif elo < 1200:
            return 6
        elif elo < 1400:
            return 9
        elif elo < 1600:
            return 12
        elif elo < 1800:
            return 15
        else:
            return 18
    
    def handle_chess_result(self, result, npc):
        """Handle the outcome of a chess match"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== MATCH RESULT: {self.player['name']} vs. {npc['name']} ===\n")
        
        # Update player stats
        if result == "win":
            self.player["chess_wins"] += 1
            print("Congratulations! You have won the match.")
            
            if npc.get("hostile", False):
                print(f"\n{npc['name']} looks shocked. \"Impossible! How could I lose to you?\"")
                
                # If this is part of a quest, mark it as completed
                if npc.get("quest") in self.player["quests"]:
                    print(f"\nYou have completed the quest: {npc['quest'].replace('_', ' ').title()}")
                    self.player["quests"].remove(npc["quest"])
                    
                    # Add a reward
                    reward = "victory_token"
                    self.player["inventory"].append(reward)
                    print(f"You received: {reward.replace('_', ' ').title()}")
            else:
                print(f"\n{npc['name']} nods respectfully. \"Well played. Your strategy was impressive.\"")
                
                # If this was a training match, provide a benefit
                if npc_id == "hermit_sage":
                    print("\nThe hermit teaches you a special chess technique that might help in future matches.")
                    self.player["inventory"].append("hermits_strategy")
                    print("You received: Hermit's Strategy")
        
        elif result == "loss":
            self.player["chess_losses"] += 1
            print("You have lost the match.")
            
            if npc.get("hostile", False):
                print(f"\n{npc['name']} smirks triumphantly. \"As expected. You were no match for me.\"")
                
                # If this was the bandit, lose an item
                if npc_id == "village_champion" and self.player["inventory"]:
                    lost_item = self.player["inventory"].pop()
                    print(f"\n{npc['name']} takes your {lost_item.replace('_', ' ')} as the spoils of victory.")
            else:
                print(f"\n{npc['name']} offers advice: \"Your opening was strong, but watch your middle game.\"")
        
        else:  # Draw
            self.player["chess_draws"] += 1
            print("The match ends in a draw.")
            print(f"\n{npc['name']}: \"A fair outcome. We seem evenly matched.\"")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Display help information"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== HELP: COMMANDS ===\n")
        print("MOVE [direction]        - Move in the specified direction (north, south, east, west)")
        print("TALK TO [person]        - Start a conversation with an NPC")
        print("EXAMINE [item/person]   - Look at something or someone more closely")
        print("TAKE [item]             - Pick up an item")
        print("INVENTORY               - Check your possessions")
        print("CHALLENGE [person]      - Challenge an NPC to a chess match")
        print("HELP                    - Show this help screen")
        print("QUIT                    - Exit the game")
        
        input("\nPress Enter to continue...")
    
    def save_game(self):
        """Save the current game state"""
        save_data = {
            "player": self.player,
            "current_location": self.current_location["name"],
            "locations": self.locations,
            "npcs": self.npcs
        }
        
        try:
            with open(f"{self.player['name']}_save.dat", "wb") as f:
                pickle.dump(save_data, f)
            print("Game saved successfully.")
        except:
            print("Error saving game.")
    
    def load_game(self, filename):
        """Load a saved game"""
        try:
            with open(filename, "rb") as f:
                save_data = pickle.load(f)
            
            self.player = save_data["player"]
            self.locations = save_data["locations"]
            self.npcs = save_data["npcs"]
            self.current_location = self.locations[save_data["current_location"]]
            
            print("Game loaded successfully.")
            return True
        except:
            print("Error loading game.")
            return False

# Main entry point
if __name__ == "__main__":
    game = ChessRPG()
    game.start_game()
