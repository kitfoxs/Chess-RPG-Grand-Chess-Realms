import os
import chess
import chess.engine
import time
import random

class ChessMatchManager:
    """
    Manages chess matches, interactions with the Stockfish engine,
    and provides utilities for chess gameplay.
    """
    
    def __init__(self, stockfish_path=None):
        """
        Initialize the chess match manager.
        
        Args:
            stockfish_path: Path to the Stockfish executable. If None, will try to find it in common locations.
        """
        self.engine = None
        self.stockfish_path = stockfish_path
        
        # Try to initialize the engine
        self.initialize_engine()
    
    def initialize_engine(self):
        """Initialize the Stockfish chess engine"""
        try:
            # If a path was provided, use it
            if self.stockfish_path:
                self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
                return
            
            # Common paths to look for Stockfish
            paths = [
                "stockfish",  # If in PATH
                "./stockfish",
                "./engines/stockfish",
                "/usr/games/stockfish",
                "/usr/local/bin/stockfish",
                "C:/Program Files/Stockfish/stockfish.exe",
                "C:/Program Files (x86)/Stockfish/stockfish.exe"
            ]
            
            # Try each path
            for path in paths:
                try:
                    self.engine = chess.engine.SimpleEngine.popen_uci(path)
                    self.stockfish_path = path
                    print(f"Successfully initialized Stockfish from: {path}")
                    return
                except:
                    continue
            
            print("Warning: Could not initialize Stockfish. Using simplified chess mode.")
        except Exception as e:
            print(f"Error initializing chess engine: {e}")
            print("Using simplified chess mode.")
    
    def close(self):
        """Close the chess engine properly"""
        if self.engine:
            self.engine.quit()
    
    def set_engine_strength(self, elo):
        """
        Set the engine strength based on Elo rating.
        
        Args:
            elo: Target Elo rating for the engine (roughly 800-3000)
        """
        if not self.engine:
            return False
        
        # Convert Elo to Stockfish skill level (0-20)
        skill_level = self.elo_to_skill_level(elo)
        
        # Configure the engine
        self.engine.configure({"Skill Level": skill_level})
        
        return True
    
    def elo_to_skill_level(self, elo):
        """
        Convert Elo rating to Stockfish skill level (0-20)
        
        Args:
            elo: Elo rating
            
        Returns:
            Stockfish skill level (0-20)
        """
        # Simple mapping
        if elo < 800:
            return 0
        elif elo < 900:
            return 1
        elif elo < 1000:
            return 2
        elif elo < 1100:
            return 3
        elif elo < 1200:
            return 4
        elif elo < 1300:
            return 5
        elif elo < 1400:
            return 6
        elif elo < 1500:
            return 8
        elif elo < 1600:
            return 10
        elif elo < 1700:
            return 12
        elif elo < 1800:
            return 14
        elif elo < 1900:
            return 16
        elif elo < 2000:
            return 18
        else:
            return 20
    
    def play_match(self, opponent_name, opponent_elo, time_control="90/30"):
        """
        Play a full chess match against the engine.
        
        Args:
            opponent_name: Name of the opponent for display
            opponent_elo: Elo rating of the opponent
            time_control: Time control format (60/30, 90/30, 120/30, or None)
            
        Returns:
            Result of the match: "win", "loss", "draw"
        """
        # Initialize the board
        board = chess.Board()
        
        # Set up engine strength
        if self.engine:
            self.set_engine_strength(opponent_elo)
        
        # Parse time control
        main_time_minutes = 90
        increment_seconds = 30
        
        if time_control:
            parts = time_control.split('/')
            if len(parts) >= 1:
                try:
                    main_time_minutes = int(parts[0])
                except:
                    pass
            if len(parts) >= 2:
                try:
                    increment_seconds = int(parts[1])
                except:
                    pass
        
        # Convert to seconds
        player_time = main_time_minutes * 60
        engine_time = main_time_minutes * 60
        
        # Introduction to the match
        self.display_match_intro(opponent_name, opponent_elo, time_control)
        
        # Main game loop
        while not board.is_game_over():
            # Display the board
            self.display_board(board)
            
            # Display remaining time if using a clock
            if time_control:
                self.display_clock(player_time, engine_time)
            
            # Player's turn (white)
            if board.turn == chess.WHITE:
                start_time = time.time()
                
                move = self.get_player_move(board)
                
                # Update player's clock
                if time_control:
                    elapsed = time.time() - start_time
                    player_time -= elapsed
                    player_time += increment_seconds
                    
                    # Check for time forfeit
                    if player_time <= 0:
                        print("You've run out of time!")
                        return "loss"
                
                # Make the move
                board.push(move)
            
            # Engine's turn (black)
            else:
                print(f"\n{opponent_name} is thinking...")
                
                start_time = time.time()
                
                if self.engine:
                    # Limit engine thinking time based on its remaining clock
                    time_limit = min(30, engine_time / 10) if time_control else 1.0
                    result = self.engine.play(board, chess.engine.Limit(time=time_limit))
                    move = result.move
                else:
                    # Fallback if no engine: make a random legal move
                    import random
                    legal_moves = list(board.legal_moves)
                    move = random.choice(legal_moves)
                
                # Update engine's clock
                if time_control:
                    elapsed = time.time() - start_time
                    engine_time -= elapsed
                    engine_time += increment_seconds
                    
                    # Check for time forfeit
                    if engine_time <= 0:
                        print(f"{opponent_name} has run out of time!")
                        return "win"
                
                # Make the move and display it
                board.push(move)
                print(f"{opponent_name} played: {move.uci()}")
                time.sleep(1)  # Small pause for readability
        
        # Display final position
        self.display_board(board)
        
        # Determine and return the result
        return self.get_match_result(board)
    
    def get_player_move(self, board):
        """
        Get a valid move from the player.
        
        Args:
            board: Current chess.Board position
            
        Returns:
            A valid chess.Move
        """
        while True:
            try:
                move_uci = input("\nYour move (e.g., e2e4, g1f3): ").strip()
                
                # Handle special commands
                if move_uci.lower() in ['quit', 'exit', 'resign']:
                    confirm = input("Are you sure you want to resign? (y/n): ").lower()
                    if confirm.startswith('y'):
                        raise KeyboardInterrupt("Player resigned")
                    continue
                
                # Check for algebraic notation (like Nf3) and convert if needed
                if len(move_uci) <= 4 and not move_uci[0].isdigit():
                    # Try to find a matching move
                    for legal_move in board.legal_moves:
                        if board.san(legal_move) == move_uci:
                            return legal_move
                
                # Try UCI format
                move = chess.Move.from_uci(move_uci)
                
                # Validate move
                if move in board.legal_moves:
                    return move
                else:
                    print("Illegal move. Try again.")
            except ValueError:
                print("Invalid format. Please use UCI notation (e.g., e2e4) or algebraic notation (e.g., Nf3).")
            except KeyboardInterrupt:
                raise
            except:
                print("Error processing move. Try again.")
    
    def display_match_intro(self, opponent_name, opponent_elo, time_control):
        """Display an introduction to the chess match"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print(f" CHESS MATCH: YOU vs. {opponent_name.upper()}")
        print("=" * 60)
        print(f"Opponent Elo: {opponent_elo}")
        if time_control:
            print(f"Time Control: {time_control}")
        print("\nYou play as White, your opponent plays as Black.")
        print("\nEnter moves in UCI format (e.g., e2e4) or algebraic notation (e.g., Nf3)")
        print("Type 'resign' to forfeit the match.")
        print("=" * 60)
        input("\nPress Enter to begin the match...")
    
    def display_board(self, board):
        """
        Display the current chess board.
        
        Args:
            board: chess.Board to display
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Convert board to string
        board_str = str(board)
        
        # Create a better representation with row/column labels
        output = []
        output.append("  a b c d e f g h")
        output.append(" +-----------------+")
        
        rows = board_str.split('\n')
        for i, row in enumerate(rows):
            output.append(f"{8-i}| {' '.join(row)} |{8-i}")
        
        output.append(" +-----------------+")
        output.append("  a b c d e f g h")
        
        # Print the board
        print('\n'.join(output))
        
        # Show additional information
        if board.is_check():
            print("\nCHECK!")
        
        # Show last move if available
        if board.move_stack:
            last_move = board.peek()
            print(f"\nLast move: {last_move.uci()}")
    
    def display_clock(self, player_time, engine_time):
        """Display the remaining time for both players"""
        player_minutes = int(player_time // 60)
        player_seconds = int(player_time % 60)
        
        engine_minutes = int(engine_time // 60)
        engine_seconds = int(engine_time % 60)
        
        print(f"\nTime remaining:")
        print(f"You: {player_minutes:02d}:{player_seconds:02d}")
        print(f"Opponent: {engine_minutes:02d}:{engine_seconds:02d}")
    
    def get_match_result(self, board):
        """
        Determine the result of a completed match.
        
        Args:
            board: chess.Board with game over position
            
        Returns:
            "win", "loss", or "draw"
        """
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return "loss"  # White to move but checkmate = white lost
            else:
                return "win"   # Black to move but checkmate = white won
        
        # Various draw conditions
        elif board.is_stalemate():
            print("Game ended in stalemate.")
            return "draw"
        elif board.is_insufficient_material():
            print("Game ended due to insufficient material to checkmate.")
            return "draw"
        elif board.is_fifty_moves():
            print("Game ended due to fifty-move rule.")
            return "draw"
        elif board.is_repetition():
            print("Game ended due to threefold repetition.")
            return "draw"
        else:
            return "draw"  # Default case
    
    def simulate_match(self, opponent_elo, player_skill):
        """
        Simulate a chess match without actually playing it.
        Useful when the engine is not available or for quick encounters.
        
        Args:
            opponent_elo: Opponent's Elo rating
            player_skill: Player's estimated skill level
            
        Returns:
            "win", "loss", or "draw" and a narrative description
        """
        # Calculate win probability based on Elo difference
        # Using a simplified version of the Elo formula
        expected_score = 1 / (1 + 10**((opponent_elo - player_skill) / 400))
        
        # Add some randomness
        import random
        roll = random.random()
        
        # Determine outcome
        if roll < expected_score:
            result = "win"
        elif roll < expected_score + 0.2:  # 20% chance of draw
            result = "draw"
        else:
            result = "loss"
        
        # Generate narrative based on the result
        narrative = self.generate_match_narrative(result, opponent_elo, player_skill)
        
        return result, narrative
    
    def generate_match_narrative(self, result, opponent_elo, player_skill):
        """
        Generate a narrative description of a simulated chess match.
        
        Args:
            result: "win", "loss", or "draw"
            opponent_elo: Opponent's Elo rating
            player_skill: Player's estimated skill level
            
        Returns:
            A string describing the match
        """
        import random
        
        # Determine the flow of the game based on skill difference
        skill_diff = player_skill - opponent_elo
        
        # Opening phase descriptions
        openings = [
            "The game began with a standard {opening} opening.",
            "You chose the {opening} for your first moves.",
            "The board quickly evolved into a {opening} position.",
            "The early game developed along the lines of the {opening}."
        ]
        
        opening_names = [
            "Ruy Lopez", "Sicilian Defense", "Queen's Gambit", 
            "King's Indian", "French Defense", "English Opening",
            "Caro-Kann", "Nimzo-Indian", "Italian Game", "Pirc Defense"
        ]
        
        # Middlegame phase descriptions
        even_middlegames = [
            "The middlegame was tense, with both sides carefully maneuvering for advantage.",
            "As the position grew complex, both you and your opponent found strong moves.",
            "A balanced struggle emerged in the center, with neither side able to claim a clear advantage.",
            "Pieces were exchanged at an even rate, maintaining the tension on the board."
        ]
        
        winning_middlegames = [
            "You seized the initiative with a powerful {piece} maneuver in the middlegame.",
            "A tactical opportunity allowed you to win material - a {piece} for nearly nothing.",
            "Your opponent made a mistake, allowing you to establish a dominant position.",
            "Your strategic understanding proved superior, gradually improving your position."
        ]
        
        losing_middlegames = [
            "Your opponent found a strong {piece} sacrifice that put you on the defensive.",
            "A tactical oversight cost you a {piece} in the middlegame complications.",
            "Your opponent's pressure mounted, forcing your pieces into awkward positions.",
            "The initiative slipped away as your opponent coordinated their pieces better."
        ]
        
        pieces = ["knight", "bishop", "rook", "queen", "pawn"]
        
        # Endgame and result descriptions
        winning_endgames = [
            "In the endgame, your material advantage proved decisive.",
            "You converted your positional advantage into a winning endgame.",
            "With precise technique, you navigated the endgame to secure victory.",
            "Your opponent resigned when it became clear you would promote a pawn."
        ]
        
        losing_endgames = [
            "The endgame revealed the weaknesses in your position, leading to defeat.",
            "Despite your efforts, your opponent's endgame technique proved superior.",
            "A critical error in time pressure sealed your fate in the endgame.",
            "Your opponent successfully converted their advantage into a win."
        ]
        
        draw_descriptions = [
            "The game ended in a draw by perpetual check.",
            "With careful defense, you held your opponent to a draw in a slightly worse position.",
            "Both sides neutralized each other's threats, leading to a drawn position.",
            "The endgame reached a theoretical draw with insufficient material."
        ]
        
        # Generate the narrative
        narrative = []
        
        # Opening
        opening = random.choice(opening_names)
        narrative.append(random.choice(openings).format(opening=opening))
        
        # Middlegame
        if result == "win":
            narrative.append(random.choice(winning_middlegames).format(piece=random.choice(pieces)))
        elif result == "loss":
            narrative.append(random.choice(losing_middlegames).format(piece=random.choice(pieces)))
        else:
            narrative.append(random.choice(even_middlegames))
        
        # Endgame
        if result == "win":
            narrative.append(random.choice(winning_endgames))
        elif result == "loss":
            narrative.append(random.choice(losing_endgames))
        else:
            narrative.append(random.choice(draw_descriptions))
        
        return " ".join(narrative)
    
    def display_chess_tip(self):
        """Display a random chess tip"""
        tips = [
            "Control the center early to maximize your options for development.",
            "Knights are stronger in closed positions, while bishops shine in open ones.",
            "A knight on the rim is dim - centralized knights are usually more effective.",
            "Don't move the same piece twice in the opening unless necessary.",
            "Castle early to protect your king and connect your rooks.",
            "Develop pieces toward the center in the opening, not toward the edges.",
            "In the endgame, activate your king - it becomes a powerful attacking piece.",
            "Look for forced moves like checks, captures, and threats before deciding your move.",
            "When ahead in material, simplify by trading pieces but not pawns.",
            "When behind in material, create complications and avoid exchanges.",
            "The threat is stronger than the execution - sometimes just threatening a tactic is enough.",
            "Passed pawns must be pushed! Their promotion potential creates significant pressure.",
            "Two weaknesses principle: If your opponent has one weakness, attack it. If they defend it successfully, create a second weakness elsewhere.",
            "If you spot a good move, look for a better one before playing it.",
            "Don't bring your queen out too early - it can become a target for enemy development with tempo.",
            "Rooks belong on open files where they can exert maximum pressure.",
            "When attacking, involve as many pieces as possible. When defending, use the minimum necessary."
        ]
        
        return random.choice(tips)
    
    def analyze_position(self, board, depth=15):
        """
        Analyze the current position using the engine.
        
        Args:
            board: chess.Board to analyze
            depth: Search depth
            
        Returns:
            Evaluation and best move
        """
        if not self.engine:
            return None, None
        
        # Run the analysis
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
            score = info["score"].white()
            best_move = info.get("pv", [None])[0]
            
            return score, best_move
        except:
            return None, None
