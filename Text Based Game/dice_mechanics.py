import random
import os
import time

class GameMechanics:
    """
    Handles dice rolls and additional game mechanics for non-chess parts of the game,
    such as exploration, social interactions, and random encounters.
    """
    
    def __init__(self, game_instance):
        self.game = game_instance
    
    def roll_dice(self, num_dice=1, sides=20, modifier=0):
        """Roll dice with a specified number of sides and add a modifier"""
        result = sum(random.randint(1, sides) for _ in range(num_dice)) + modifier
        return result
    
    def display_roll(self, roll_type, target, result, success_threshold=None):
        """Display the result of a dice roll with animation"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== {roll_type.upper()} CHECK ===\n")
        print(f"Rolling for: {target}")
        
        # Animation for rolling dice
        for _ in range(3):
            print("Rolling...", end="\r")
            time.sleep(0.3)
            print("Rolling.  ", end="\r")
            time.sleep(0.3)
            print("Rolling.. ", end="\r")
            time.sleep(0.3)
        
        print(f"\nResult: {result}")
        
        if success_threshold is not None:
            if result >= success_threshold:
                print("SUCCESS!")
            else:
                print("FAILURE.")
        
        input("\nPress Enter to continue...")
        return result >= success_threshold if success_threshold is not None else result
    
    def exploration_check(self, target, difficulty):
        """
        Handle exploration checks like searching for hidden items,
        navigating difficult terrain, etc.
        """
        roll = self.roll_dice(1, 20)
        success = self.display_roll("Exploration", target, roll, difficulty)
        
        return success
    
    def social_check(self, target, difficulty):
        """
        Handle social interaction checks like persuasion, intimidation,
        gathering information, etc.
        """
        # Add background-based modifiers
        modifier = 0
        if self.game.player["background"] == "Noble Strategist":
            modifier = 2  # Nobles are better at social interactions
        
        roll = self.roll_dice(1, 20, modifier)
        success = self.display_roll("Social", target, roll, difficulty)
        
        return success
    
    def random_encounter_check(self):
        """
        Check if a random encounter occurs while traveling
        Returns the encounter type or None if no encounter
        """
        # 20% chance of random encounter when moving between locations
        if random.random() < 0.2:
            # Roll a d6 to determine encounter type
            roll = self.roll_dice(1, 6)
            
            encounters = {
                1: "traveler",
                2: "merchant",
                3: "chess_puzzle",
                4: "minor_challenge",
                5: "lore_discovery",
                6: "special_event"
            }
            
            return encounters[roll]
        
        return None
    
    def handle_random_encounter(self, encounter_type):
        """Process a random encounter based on type"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== UNEXPECTED ENCOUNTER ===\n")
        
        if encounter_type == "traveler":
            travelers = [
                "a wandering minstrel with tales of distant chess tournaments",
                "a messenger carrying sealed letters between kingdoms",
                "a refugee from a village near the Checkered Frontier",
                "a pilgrim journeying to the Sanctuary of St. Alekhine"
            ]
            traveler = random.choice(travelers)
            
            print(f"You encounter {traveler}.")
            
            # Simple dialogue options
            print("\nHow do you respond?")
            print("1. Greet them warmly")
            print("2. Ask about recent news")
            print("3. Inquire about chess strategies")
            print("4. Continue on your way")
            
            choice = 0
            while choice < 1 or choice > 4:
                try:
                    choice = int(input("\nSelect a number: "))
                except:
                    pass
            
            if choice == 1:
                print("\nYour friendly demeanor puts the traveler at ease.")
                print("They share a small tidbit of local lore with you.")
                # Could add lore here
            
            elif choice == 2:
                print("\nThe traveler shares the latest news from nearby settlements.")
                # Could add news/quest hooks here
            
            elif choice == 3:
                print("\nThe traveler discusses a chess strategy they've observed.")
                print("You gain insight into a particular opening or endgame technique.")
                # Could add a small benefit here
            
            else:
                print("\nYou nod politely and continue on your journey.")
        
        elif encounter_type == "merchant":
            print("You encounter a traveling merchant with a cart full of wares.")
            print("Among their goods, you spot several chess sets of varying quality.")
            
            # Simple trading interaction
            print("\nThe merchant offers:")
            print("1. Intricate wooden chess set (5 gold)")
            print("2. Chess strategy manual (3 gold)")
            print("3. Mysterious chess piece (2 gold)")
            print("4. Decline and continue your journey")
            
            choice = 0
            while choice < 1 or choice > 4:
                try:
                    choice = int(input("\nSelect a number: "))
                except:
                    pass
            
            # Simulate a simple purchase
            if choice < 4:
                print("\nYou don't have enough gold for this purchase yet.")
                print("The merchant nods understanding. \"Perhaps next time.\"")
                # In a full implementation, check gold and handle purchase
        
        elif encounter_type == "chess_puzzle":
            print("You discover a weathered stone with a chess puzzle carved into it.")
            print("The position seems to be a mate-in-two problem.")
            
            # Simulate solving a chess puzzle
            print("\nDo you try to solve the puzzle?")
            print("1. Yes, I'll take the time to figure it out")
            print("2. No, I'll continue on my way")
            
            choice = 0
            while choice < 1 or choice > 2:
                try:
                    choice = int(input("\nSelect a number: "))
                except:
                    pass
            
            if choice == 1:
                # Roll to see if player solves the puzzle
                difficulty = 12  # Moderate difficulty
                roll = self.roll_dice(1, 20)
                
                if roll >= difficulty:
                    print("\nAfter careful consideration, you solve the puzzle!")
                    print("You feel a sense of satisfaction and insight.")
                    # Could add a small benefit here
                else:
                    print("\nDespite your efforts, the solution eludes you.")
                    print("Perhaps you'll encounter similar puzzles in the future.")
            else:
                print("\nYou decide to leave the puzzle for another traveler.")
        
        elif encounter_type == "minor_challenge":
            print("As you travel, you're intercepted by a local chess enthusiast.")
            print("They challenge you to a friendly match to pass the time.")
            
            # Offer a quick simulated chess match
            print("\nDo you accept the challenge?")
            print("1. Yes, I'll play a quick game")
            print("2. No, I must continue my journey")
            
            choice = 0
            while choice < 1 or choice > 2:
                try:
                    choice = int(input("\nSelect a number: "))
                except:
                    pass
            
            if choice == 1:
                # Simple simulated chess match
                print("\nYou set up a portable chess board and begin to play.")
                
                # Determine outcome (simplified)
                result = random.choice(["win", "loss", "draw"])
                
                if result == "win":
                    print("You outmaneuver your opponent and secure a victory!")
                    print("They congratulate you and offer a small token of respect.")
                    # Add small reward
                
                elif result == "loss":
                    print("Your opponent proves surprisingly skilled and defeats you.")
                    print("They offer advice on improving your strategy.")
                
                else:  # Draw
                    print("The game ends in a draw after a series of careful exchanges.")
                    print("You both part ways with newfound respect.")
            else:
                print("\nYou politely decline, citing your urgent journey.")
                print("The enthusiast nods understanding and wishes you well.")
        
        elif encounter_type == "lore_discovery":
            discoveries = [
                "a fragment of an ancient manuscript describing the First Game",
                "an old map showing the location of a chess shrine",
                "a carved wooden tile depicting a historical chess match",
                "an old battlefield marker where a famous chess duel once occurred"
            ]
            discovery = random.choice(discoveries)
            
            print(f"You discover {discovery}.")
            print("This find adds to your understanding of the Grand Chess Realms.")
            
            # Add the discovery to player's knowledge
            if "lore_discoveries" not in self.game.player:
                self.game.player["lore_discoveries"] = []
            
            self.game.player["lore_discoveries"].append(discovery)
        
        elif encounter_type == "special_event":
            events = [
                "witness a small tournament between local villagers",
                "observe a royal procession with chess-themed banners",
                "stumble upon a secret meeting between diplomats using chess as cover",
                "find a master teaching children the basics of strategy"
            ]
            event = random.choice(events)
            
            print(f"You {event}.")
            print("The scene offers insight into how chess permeates this world.")
            
            # Potentially add a unique benefit or quest hook here
        
        input("\nPress Enter to continue...")
    
    def loot_roll(self, quality="common"):
        """Roll for random loot based on quality level"""
        # Define loot tables for different quality levels
        loot_tables = {
            "common": [
                "wooden_pawn",
                "basic_chess_manual",
                "traveler's_rations",
                "small_pouch_of_coins"
            ],
            "uncommon": [
                "marble_knight",
                "regional_strategy_guide",
                "map_to_hidden_grove",
                "silver_inlaid_chess_piece"
            ],
            "rare": [
                "enchanted_bishop",
                "ancient_chess_manuscript",
                "royal_tournament_invitation",
                "crystalline_chess_set"
            ]
        }
        
        # Select appropriate table and roll
        table = loot_tables.get(quality, loot_tables["common"])
        item = random.choice(table)
        
        return item
    
    def critical_moment(self, description):
        """
        Handle critical narrative moments with dice rolls
        that can affect the story
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== CRITICAL MOMENT ===\n")
        print(description)
        
        print("\nThis is a pivotal moment. Your actions here may have lasting consequences.")
        input("\nPress Enter to roll the dice of fate...")
        
        roll = self.roll_dice(1, 20)
        
        # Determine outcome tiers
        if roll >= 18:  # Critical success
            result = "great_success"
            print(f"\nRoll: {roll} - A spectacular success!")
        elif roll >= 12:  # Success
            result = "success"
            print(f"\nRoll: {roll} - Success!")
        elif roll >= 8:  # Partial success
            result = "partial"
            print(f"\nRoll: {roll} - Partial success.")
        else:  # Failure
            result = "failure"
            print(f"\nRoll: {roll} - Failure.")
        
        input("\nPress Enter to continue...")
        return result

# The mechanics class would be instantiated in the main game
# and used like this:
#
# mechanics = GameMechanics(game_instance)
# 
# # For exploration
# if mechanics.exploration_check("Find hidden passage", 15):
#     print("You discover a secret door!")
# 
# # For social
# if mechanics.social_check("Convince the guard", 12):
#     print("The guard lets you pass.")
# 
# # For random encounters
# encounter = mechanics.random_encounter_check()
# if encounter:
#     mechanics.handle_random_encounter(encounter)
