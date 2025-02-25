import os
import sys
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("GrandChessRealms")

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

# Import the game components
from game_structure import ChessRPG
from dice_mechanics import GameMechanics
from lore_and_story import LoreManager, StoryManager
from chess_engine_integration import ChessMatchManager

try:
    from chessnut_integration import integrate_with_chess_manager
    CHESSNUT_AVAILABLE = True
except ImportError:
    logger.warning("Chessnut integration module not found. Continuing without Chessnut support.")
    CHESSNUT_AVAILABLE = False


class GrandChessRealms:
    """
    Main game class that integrates all components and runs the Grand Chess Realms RPG.
    """
    
    def __init__(self):
        """Initialize the complete game"""
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display loading message
        print("Loading Grand Chess Realms...")
        print("Initializing components...")
        
        # Initialize core game
        self.game = ChessRPG()
        
        # Initialize chess engine
        print("Setting up chess engine...")
        self.chess_manager = ChessMatchManager()
        
        # Initialize Chessnut Pro integration
        if CHESSNUT_AVAILABLE:
            print("Looking for Chessnut Pro board...")
            try:
                self.chess_manager = integrate_with_chess_manager(self.chess_manager)
                if hasattr(self.chess_manager, 'chessnut') and self.chess_manager.chessnut.connected:
                    print("✅ Chessnut Pro connected and ready! You can use the physical board for moves.")
                else:
                    print("❌ No Chessnut Pro board detected. Using keyboard input for chess moves.")
                    print("   You can check connection status with the 'chessnut' command during gameplay.")
            except Exception as e:
                logger.error(f"Error setting up Chessnut Pro: {e}")
                print(f"Error setting up Chessnut Pro: {e}")
                print("Continuing without Chessnut integration.")
        else:
            print("Chessnut integration not available. Using keyboard input for chess moves.")
        
        # Initialize dice mechanics for non-chess events
        print("Preparing game mechanics...")
        self.mechanics = GameMechanics(self.game)
        
        # Initialize lore and story
        print("Loading world lore and stories...")
        self.lore = LoreManager()
        self.story = StoryManager(self.game, self.lore)
        
        # Bind components to main game
        self.game.chess_manager = self.chess_manager
        self.game.mechanics = self.mechanics
        self.game.lore = self.lore
        self.game.story = self.story
        
        # Extend the game's command processing
        self.original_process_command = self.game.process_command
        self.game.process_command = self.extended_process_command
        
        # Enhance the move player function to check for random encounters
        self.original_move_player = self.game.move_player
        self.game.move_player = self.enhanced_move_player
        
        # Enhance the challenge function to use the chess manager
        self.original_challenge_to_chess = self.game.challenge_to_chess
        self.game.challenge_to_chess = self.enhanced_challenge_to_chess
        
        print("All systems initialized successfully!")
        time.sleep(1)
    
    def extended_process_command(self, command):
        """Extended command processing with additional commands"""
        # Split the command into words
        words = command.split()
        
        if not words:
            return
        
        action = words[0].lower()
        
        # Handle additional commands
        if action == "lore" or action == "codex":
            self.show_lore_menu()
        
        elif action == "quest" or action == "quests":
            self.show_quests()
        
        elif action == "read" and len(words) > 1:
            self.read_item(" ".join(words[1:]))
        
        elif action == "status":
            self.show_player_status()
        
        elif action == "tip":
            self.show_chess_tip()
        
        elif action == "roll" and len(words) > 1:
            self.handle_dice_roll(" ".join(words[1:]))
        
        elif action == "chessnut":
            self.check_chessnut_status()
        
        elif action == "save":
            self.save_game()
        
        elif action == "load":
            if len(words) > 1:
                self.load_game(words[1])
            else:
                print("Please specify a save file to load.")
                input("Press Enter to continue...")
        
        elif action == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        
        else:
            # Default to original command handling
            self.original_process_command(command)
    
    def check_chessnut_status(self):
        """Check and display Chessnut Pro connection status"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" CHESSNUT PRO STATUS ")
        print("=" * 60)
        
        if not CHESSNUT_AVAILABLE:
            print("\n❌ Chessnut Pro integration module is not installed")
            print("\nTo enable Chessnut Pro integration, make sure chessnut_integration.py")
            print("is in your game directory and EasyLinkSDK is properly installed.")
            input("\nPress Enter to continue...")
            return
        
        if hasattr(self.chess_manager, 'chessnut'):
            chessnut = self.chess_manager.chessnut
            
            # Get detailed status
            status = chessnut.get_connection_status()
            
            if status['connected']:
                print("\n✅ Chessnut Pro is connected and ready")
                print("\nYou can use your physical board to make moves during chess matches.")
                print("The game will automatically detect when you move pieces on the board.")
                print("If a move isn't detected, you can still enter moves manually.")
            else:
                print("\n❌ Chessnut Pro is not connected")
                
                if status['sdk_available']:
                    print("\nSDK Status: Available")
                    print(f"Last Error: {status['last_error'] or 'None'}")
                    print(f"Connection Attempts: {status['connection_attempts']}")
                    
                    print("\nAttempting to reconnect...")
                    if chessnut.connect(auto_retry=False):
                        # Check if actually connected after a short delay
                        time.sleep(2)
                        if chessnut.connected:
                            print("Successfully reconnected to Chessnut Pro!")
                        else:
                            print("Connection initiated but not established yet.")
                            print("Please check your board and try again later.")
                    else:
                        print("Reconnection failed. Please check your board and try again.")
                        print("Make sure the board is powered on and within Bluetooth range.")
                else:
                    print("\nChessnut SDK is not available. Please install EasyLinkSDK.")
            
            # Provide troubleshooting tips
            print("\nTroubleshooting Tips:")
            print("1. Make sure your Chessnut Pro is powered on")
            print("2. Ensure Bluetooth is enabled on your computer")
            print("3. Place the board within range of your computer")
            print("4. Check that the board has sufficient battery")
            print("5. Restart the board and try connecting again")
        else:
            print("\n❌ Chessnut Pro integration is not available")
            print("\nThe Chessnut Pro integration module may not be properly installed.")
            print("Please refer to the setup guide for instructions.")
        
        input("\nPress Enter to continue...")
    
    def enhanced_move_player(self, direction):
        """Enhanced move player function that checks for random encounters"""
        # Call the original move function
        old_location = self.game.current_location
        self.original_move_player(direction)
        
        # If player successfully moved to a new location
        if old_location != self.game.current_location:
            # Check for story triggers in the new location
            self.story.check_story_triggers(self.game.current_location["name"])
            
            # Check for random encounters
            encounter_type = self.mechanics.random_encounter_check()
            if encounter_type:
                self.mechanics.handle_random_encounter(encounter_type)
    
    def enhanced_challenge_to_chess(self, npc_name):
        """Enhanced chess challenge function using the chess manager"""
        # Find the NPC
        npc_id = None
        for npc in self.game.current_location["npcs"]:
            if npc_name.lower() in self.game.npcs[npc]["name"].lower():
                npc_id = npc
                break
        
        if not npc_id:
            print(f"There's no one named {npc_name} here to challenge.")
            input("Press Enter to continue...")
            return
        
        npc = self.game.npcs[npc_id]
        
        # Chess match setup
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(f" CHESS CHALLENGE: {self.game.player['name']} vs. {npc['name']} ")
        print("=" * 60)
        
        # Check if Chessnut is available
        has_chessnut = (CHESSNUT_AVAILABLE and hasattr(self.chess_manager, 'chessnut') and 
                        self.chess_manager.chessnut.connected)
        
        if has_chessnut:
            print("\n✓ Chessnut Pro board detected - you can make moves physically on your board")
            print("  The game will instruct you when to update your board with opponent moves")
        
        # Narrative introduction to the match
        print(f"\n{npc['name']} accepts your challenge.")
        print("As you both take your places at the board, a sense of anticipation fills the air.")
        
        if npc.get("hostile", False):
            print(f"\n{npc['name']}: \"You'll regret challenging me, {self.game.player['name']}. Your defeat is inevitable.\"")
        else:
            print(f"\n{npc['name']}: \"May the best strategist win.\"")
        
        input("\nPress Enter to begin the match...")
        
        # Use the chess manager to handle the match
        if self.chess_manager.engine:
            # Play a full chess match
            result = self.chess_manager.play_match(
                opponent_name=npc['name'],
                opponent_elo=npc['chess_skill'],
                time_control="90/30"  # Default time control
            )
        else:
            # No chess engine, simulate the match
            print("\nNo chess engine found. The match will be simulated.")
            time.sleep(2)
            
            # Estimate player's skill level (could be more sophisticated)
            player_skill = 1200 + (self.game.player["chess_wins"] * 50)
            
            # Simulate the match
            result, narrative = self.chess_manager.simulate_match(
                opponent_elo=npc['chess_skill'],
                player_skill=player_skill
            )
            
            # Display the narrative
            print("\n" + narrative)
            input("\nPress Enter to continue...")
        
        # Handle the result
        self.handle_chess_result(result, npc, npc_id)
    
    def handle_chess_result(self, result, npc, npc_id):
        """Handle the outcome of a chess match"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(f" MATCH RESULT: {self.game.player['name']} vs. {npc['name']} ")
        print("=" * 60)
        
        # Update player stats
        if result == "win":
            self.game.player["chess_wins"] += 1
            print("\nCongratulations! You have won the match.")
            
            if npc.get("hostile", False):
                print(f"\n{npc['name']} looks shocked. \"Impossible! How could I lose to you?\"")
                
                # If this is part of a quest, mark it as completed
                if npc.get("quest") in self.game.player["quests"]:
                    print(f"\nYou have completed the quest: {npc['quest'].replace('_', ' ').title()}")
                    self.game.player["quests"].remove(npc["quest"])
                    
                    # Add a reward
                    reward = "victory_token"
                    self.game.player["inventory"].append(reward)
                    print(f"You received: {reward.replace('_', ' ').title()}")
                
                # Special handling for story-related NPCs
                if npc_id == "village_champion":
                    # Trigger the rowan aftermath event with victory
                    self.story.trigger_story_event("rowan_aftermath", {"victory": True})
            else:
                print(f"\n{npc['name']} nods respectfully. \"Well played. Your strategy was impressive.\"")
                
                # If this was a training match, provide a benefit
                if npc_id == "hermit_sage":
                    # Trigger the hermit training event
                    self.story.trigger_story_event("hermit_training")
        
        elif result == "loss":
            self.game.player["chess_losses"] += 1
            print("\nYou have lost the match.")
            
            if npc.get("hostile", False):
                print(f"\n{npc['name']} smirks triumphantly. \"As expected. You were no match for me.\"")
                
                # If this was the bandit, lose an item
                if npc_id == "village_champion" and self.game.player["inventory"]:
                    lost_item = self.game.player["inventory"].pop()
                    print(f"\n{npc['name']} takes your {lost_item.replace('_', ' ')} as the spoils of victory.")
                
                # Special handling for story-related NPCs
                if npc_id == "village_champion":
                    # Trigger the rowan aftermath event with loss
                    self.story.trigger_story_event("rowan_aftermath", {"victory": False})
            else:
                print(f"\n{npc['name']} offers advice: \"Your opening was strong, but watch your middle game.\"")
        
        else:  # Draw
            self.game.player["chess_draws"] += 1
            print("\nThe match ends in a draw.")
            print(f"\n{npc['name']}: \"A fair outcome. We seem evenly matched.\"")
            
            # Special handling for the wandering knight
            if npc_id == "wandering_knight":
                print("\nSir Galwynne seems impressed by your ability to hold your ground.")
                print("\"A draw against me is no small feat. Perhaps you are ready to choose a path.\"")
                
                # Offer alignment choice
                self.offer_alignment_choice()
        
        input("\nPress Enter to continue...")
    
    def offer_alignment_choice(self):
        """Offer the player a choice of alignment"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" A CHOICE OF PATHS ")
        print("=" * 60)
        
        print("\nSir Galwynne studies you thoughtfully before speaking:")
        print("\"You stand at a crossroads, both literally and figuratively.")
        print("The path you choose will shape your journey through the Chess Realms.\"")
        
        print("\nChoose your path:")
        print("1. The White Kingdom - Follow the path of order, honor, and tradition")
        print("2. The Black Kingdom - Embrace ambition, adaptability, and pragmatism")
        print("3. The Neutral Path - Balance between the kingdoms, beholden to neither")
        
        choice = 0
        while choice < 1 or choice > 3:
            try:
                choice = int(input("\nYour choice (1-3): "))
            except:
                pass
        
        if choice == 1:
            self.story.trigger_story_event("alignment_choice", {"choice": "white"})
        elif choice == 2:
            self.story.trigger_story_event("alignment_choice", {"choice": "black"})
        else:
            self.story.trigger_story_event("alignment_choice", {"choice": "neutral"})
    
    def show_lore_menu(self):
        """Show the lore codex menu"""
        viewing_lore = True
        
        while viewing_lore:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=" * 60)
            print(" LORE CODEX ")
            print("=" * 60)
            
            print(f"\nDiscovered lore entries: {self.lore.get_discovered_lore_count()}\n")
            
            print("Categories:")
            print("1. History")
            print("2. Locations")
            print("3. Characters")
            print("4. Items")
            print("5. Books")
            print("6. Return to game")
            
            choice = 0
            while choice < 1 or choice > 6:
                try:
                    choice = int(input("\nSelect a category: "))
                except:
                    pass
            
            if choice == 6:
                viewing_lore = False
                continue
            
            # Map choice to category
            categories = {1: "history", 2: "locations", 3: "characters", 4: "items", 5: "books"}
            category = categories[choice]
            
            # Get entries for the category
            entries = []
            if category == "history":
                entries = [(id, entry["title"]) for id, entry in self.lore.history.items() if f"{category}:{id}" in self.lore.discovered_lore]
            elif category == "locations":
                entries = [(id, entry["title"]) for id, entry in self.lore.locations.items() if f"{category}:{id}" in self.lore.discovered_lore]
            elif category == "characters":
                entries = [(id, entry["title"]) for id, entry in self.lore.characters.items() if f"{category}:{id}" in self.lore.discovered_lore]
            elif category == "items":
                entries = [(id, entry["title"]) for id, entry in self.lore.items.items() if f"{category}:{id}" in self.lore.discovered_lore]
            elif category == "books":
                entries = [(id, entry["title"]) for id, entry in self.lore.books.items() if f"books:{id}" in self.lore.discovered_lore]
            
            if not entries:
                print("\nYou haven't discovered any lore in this category yet.")
                input("\nPress Enter to continue...")
                continue
            
            # Show entries in this category
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=" * 60)
            print(f" {category.upper()} ")
            print("=" * 60)
            
            for i, (id, title) in enumerate(entries, 1):
                print(f"{i}. {title}")
            
            print(f"{len(entries) + 1}. Back to categories")
            
            entry_choice = 0
            while entry_choice < 1 or entry_choice > len(entries) + 1:
                try:
                    entry_choice = int(input("\nSelect an entry: "))
                except:
                    pass
            
            if entry_choice == len(entries) + 1:
                continue  # Back to categories
            
            # Display the selected entry
            entry_id, _ = entries[entry_choice - 1]
            entry = self.lore.get_lore_entry(category, entry_id)
            
            if entry:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 60)
                print(f" {entry['title'].upper()} ")
                print("=" * 60)
                print()
                print(entry['content'])
                input("\nPress Enter to continue...")
    
    def show_quests(self):
        """Show current quests"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" QUESTS ")
        print("=" * 60)
        
        # Main objective
        main_objective = self.story.get_current_objective()
        print("\nMain Objective:")
        print(f"- {main_objective}")
        
        # Active quests
        if self.game.player["quests"]:
            print("\nActive Quests:")
            for quest_id in self.game.player["quests"]:
                quest = self.lore.get_quest_info(quest_id)
                if quest:
                    print(f"- {quest['title']}: {quest['description']}")
                else:
                    print(f"- {quest_id.replace('_', ' ').title()}")
        else:
            print("\nNo active side quests.")
        
        # Side objectives
        side_objectives = self.story.get_side_objectives()
        if side_objectives:
            print("\nOptional Objectives:")
            for objective in side_objectives:
                print(f"- {objective}")
        
        input("\nPress Enter to continue...")
    
    def read_item(self, item_name):
        """Read a book or scroll"""
        # Check if the item is in inventory
        item_id = None
        for item in self.game.player["inventory"]:
            if item_name.lower() in item.lower():
                item_id = item
                break
        
        if not item_id:
            print(f"You don't have {item_name} in your inventory.")
            input("Press Enter to continue...")
            return
        
        # Check if it's a readable item
        if "book" in item_id or "scroll" in item_id:
            # Map inventory items to lore books
            book_mapping = {
                "lore_book_white_kingdom": "chronicles_white_kingdom",
                "mysterious_scroll": "mysteries_of_the_checkered_fate"
            }
            
            if item_id in book_mapping:
                book_id = book_mapping[item_id]
                book = self.lore.get_book_content(book_id)
                
                if book:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("=" * 60)
                    print(f" {book['title'].upper()} ")
                    print("=" * 60)
                    print(f"By {book['author']}\n")
                    print(book['content'])
                    
                    # Special handling for the mysterious scroll
                    if item_id == "mysterious_scroll":
                        # Mark prophecy as discovered
                        self.story.trigger_story_event("discover_prophecy")
                    
                    input("\nPress Enter to continue...")
                    return
            
            # Generic readable item
            print(f"You read the {item_id.replace('_', ' ')}. It contains some interesting information.")
            input("Press Enter to continue...")
        else:
            print(f"The {item_id.replace('_', ' ')} isn't something you can read.")
            input("Press Enter to continue...")
    
    def show_player_status(self):
        """Show detailed player status"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" CHARACTER STATUS ")
        print("=" * 60)
        
        player = self.game.player
        
        print(f"\nName: {player['name']}")
        print(f"Background: {player['background']}")
        print(f"Alignment: {player['alignment'].title()}")
        
        print("\nChess Record:")
        print(f"Wins: {player['chess_wins']}")
        print(f"Losses: {player['chess_losses']}")
        print(f"Draws: {player['chess_draws']}")
        
        # Calculate a simple Elo rating
        base_rating = 1200
        k_factor = 32
        
        wins_adjustment = player['chess_wins'] * k_factor
        losses_adjustment = player['chess_losses'] * k_factor
        draws_adjustment = player['chess_draws'] * (k_factor / 2)
        
        estimated_rating = base_rating + wins_adjustment - losses_adjustment + draws_adjustment
        estimated_rating = min(2200, max(800, estimated_rating))  # Cap between 800 and 2200
        
        print(f"Estimated Rating: {int(estimated_rating)}")
        
        print("\nInventory:")
        if player["inventory"]:
            for item in player["inventory"]:
                print(f"- {item.replace('_', ' ').title()}")
        else:
            print("- Empty")
        
        print("\nJourney Progress:")
        locations_visited = len(player['visited_locations'])
        print(f"Locations visited: {locations_visited}")
        print(f"Lore discovered: {self.lore.get_discovered_lore_count()} entries")
        print(f"Current chapter: {self.story.current_chapter.split('chapter')[1]}")
        
        # Show Chessnut Pro status
        if CHESSNUT_AVAILABLE and hasattr(self.chess_manager, 'chessnut'):
            print("\nChessnut Pro Status:")
            if self.chess_manager.chessnut.connected:
                print("✅ Connected and ready for physical moves")
            else:
                print("❌ Not connected (type 'chessnut' to check status)")
        
        input("\nPress Enter to continue...")
    
    def show_chess_tip(self):
        """Show a random chess tip"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" CHESS TIP ")
        print("=" * 60)
        
        tip = self.chess_manager.display_chess_tip()
        print(f"\n{tip}")
        
        input("\nPress Enter to continue...")
    
    def handle_dice_roll(self, roll_type):
        """Handle manual dice rolls"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" DICE ROLL ")
        print("=" * 60)
        
        # Parse roll syntax (e.g., "roll d20", "roll 2d6")
        parts = roll_type.lower().split('d')
        
        if len(parts) != 2:
            print("\nInvalid roll format. Use 'd20' or '2d6', etc.")
            input("Press Enter to continue...")
            return
        
        num_dice = 1
        if parts[0]:
            try:
                num_dice = int(parts[0])
            except:
                num_dice = 1
        
        try:
            sides = int(parts[1])
        except:
            print("\nInvalid number of sides. Try 'd20' or 'd6', etc.")
            input("Press Enter to continue...")
            return
        
        # Perform the roll
        roll = self.mechanics.roll_dice(num_dice, sides)
        
        print(f"\nRolling {num_dice}d{sides}...")
        time.sleep(1)
        print(f"Result: {roll}")
        
        input("\nPress Enter to continue...")
    
    def save_game(self):
        """Save the current game state"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" SAVE GAME ")
        print("=" * 60)
        
        # If no name yet, ask for one
        if not self.game.player["name"]:
            print("\nYou need to create a character before saving.")
            input("Press Enter to continue...")
            return
            
        # Get save filename
        default_filename = f"{self.game.player['name']}_save.dat"
        filename = input(f"\nEnter filename to save as (default: {default_filename}): ").strip()
        
        if not filename:
            filename = default_filename
        
        # Ensure it has the .dat extension
        if not filename.endswith('.dat'):
            filename += '.dat'
        
        # Call the game's save function
        self.game.save_game(filename)
        
        input("\nPress Enter to continue...")
    
    def load_game(self, filename):
        """Load a saved game"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(" LOAD GAME ")
        print("=" * 60)
        
        # Ensure it has the .dat extension
        if not filename.endswith('.dat'):
            filename += '.dat'
        
        # Check if the file exists
        if not os.path.exists(filename):
            print(f"\nSave file '{filename}' not found.")
            input("Press Enter to continue...")
            return
        
        # Call the game's load function
        if self.game.load_game(filename):
            print("\nGame loaded successfully!")
        else:
            print("\nError loading game.")
        
        input("Press Enter to continue...")
    
    def run(self):
        """Run the game"""
        try:
            # Start the game
            self.game.start_game()
        except KeyboardInterrupt:
            print("\nExiting game...")
        finally:
            # Clean up
            if self.chess_manager:
                # Disconnect from Chessnut if connected
                if CHESSNUT_AVAILABLE and hasattr(self.chess_manager, 'chessnut'):
                    try:
                        self.chess_manager.chessnut.disconnect()
                        logger.info("Disconnected from Chessnut Pro")
                    except Exception as e:
                        logger.error(f"Error disconnecting from Chessnut Pro: {e}")
                
                # Quit the chess engine
                self.chess_manager.close()
            
            print("Thank you for playing Grand Chess Realms!")


# Main entry point
if __name__ == "__main__":
    try:
        # Create and run the game
        game = GrandChessRealms()
        game.run()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        if input("Show detailed error? (y/n): ").lower().startswith('y'):
            import traceback
            traceback.print_exc()