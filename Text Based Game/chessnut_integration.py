"""
Chessnut Pro Integration Module for Grand Chess Realms
This module connects the Chessnut Pro electronic chess board to the game
using the EasyLinkSDK with enhanced reliability and error handling.
"""

import os
import sys
import time
import threading
import queue
from typing import Optional, Callable, Dict, List, Any
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("ChessnutIntegration")

# Import EasyLinkSDK - adjust path as needed based on your installation
try:
    # Try to import from installed package
    from easylink import EasyLink, BoardState, ChessMove, ChessPiece, BoardEvent
    EASYLINK_AVAILABLE = True
except ImportError:
    # If not installed, try to import from a local copy
    sys.path.append(os.path.join(os.path.dirname(__file__), 'EasyLinkSDK'))
    try:
        from easylink import EasyLink, BoardState, ChessMove, ChessPiece, BoardEvent
        EASYLINK_AVAILABLE = True
    except ImportError:
        logger.warning("EasyLinkSDK not found. Chessnut Pro integration will not be available.")
        EASYLINK_AVAILABLE = False
        # Create dummy classes for type hints if imports failed
        class EasyLink:
            def __init__(self, *args, **kwargs): pass
            def connect(self, *args, **kwargs): return False
            def disconnect(self): pass
            def get_board_state(self): return None
            def register_event_callback(self, callback): pass
            def set_position(self, fen): pass
            def scan_devices(self): return []
        
        class BoardState: pass
        class ChessMove: 
            def __init__(self):
                self.from_square = ""
                self.to_square = ""
                self.piece = None
        class ChessPiece:
            def __init__(self):
                self.type = ""
        class BoardEvent:
            def __init__(self):
                self.event_type = ""
                self.move = None
                self.board_state = None


class ChessnutInterface:
    """Interface for the Chessnut Pro electronic chess board with enhanced reliability"""
    
    def __init__(self):
        """Initialize the Chessnut interface"""
        self.easylink = None
        self.connected = False
        self.move_queue = queue.Queue()
        self.board_state = None
        self.move_callback = None
        self.error_callback = None
        self.connection_thread = None
        self.listener_thread = None
        self.running = False
        self.last_sync_time = 0
        self.connection_lock = threading.Lock()
        self.last_error = None
        self.auto_reconnect = True
        
        # Track connection attempts to avoid infinite retries
        self.connection_attempts = 0
        self.max_connection_attempts = 3
        
        # Track if SDK is available
        self.sdk_available = EASYLINK_AVAILABLE
    
    def set_callbacks(self, move_callback: Callable[[str], None], 
                      error_callback: Callable[[str], None]):
        """
        Set the callbacks for move events and errors
        
        Args:
            move_callback: Function to call when a move is made on the board
            error_callback: Function to call when an error occurs
        """
        self.move_callback = move_callback
        self.error_callback = error_callback
    
    def connect(self, device_name: Optional[str] = None, auto_retry: bool = True):
        """
        Connect to the Chessnut Pro board
        
        Args:
            device_name: Optional device name to connect to
            auto_retry: Whether to automatically retry connection if it fails
        
        Returns:
            True if connection was successful or initiated, False if SDK not available
        """
        # Check if SDK is available
        if not self.sdk_available:
            logger.warning("Chessnut SDK not available. Cannot connect.")
            if self.error_callback:
                self.error_callback("Chessnut SDK not available. Please install EasyLinkSDK.")
            return False
        
        # Reset connection attempts
        self.connection_attempts = 0
        self.auto_reconnect = auto_retry
        
        # Start connection in a separate thread to avoid blocking the game
        self.running = True
        
        with self.connection_lock:
            # Clean up any existing thread
            if self.connection_thread and self.connection_thread.is_alive():
                logger.debug("Connection thread already running, not starting a new one")
                return self.connected
                
            self.connection_thread = threading.Thread(
                target=self._connect_thread, 
                args=(device_name, auto_retry)
            )
            self.connection_thread.daemon = True
            self.connection_thread.start()
        
        # Give it a moment to try to connect
        time.sleep(1)
        return True  # Returns if connection attempt was initiated, not necessarily successful
    
    def _connect_thread(self, device_name: Optional[str], auto_retry: bool):
        """Thread function for connecting to the board"""
        try:
            with self.connection_lock:
                self.connection_attempts += 1
                
                # Clean up any existing connection
                if self.easylink:
                    try:
                        self.easylink.disconnect()
                    except:
                        pass
                    self.easylink = None
                
                logger.info(f"Attempting to connect to Chessnut Pro (attempt {self.connection_attempts})")
                self.easylink = EasyLink()
                
                if device_name:
                    # Connect to a specific device
                    logger.info(f"Connecting to device: {device_name}")
                    self.connected = self.easylink.connect(device_name)
                else:
                    # Scan for devices and connect to the first one found
                    logger.info("Scanning for Chessnut devices...")
                    devices = self.easylink.scan_devices()
                    if devices:
                        logger.info(f"Found devices: {devices}")
                        self.connected = self.easylink.connect(devices[0])
                    else:
                        logger.warning("No Chessnut devices found")
                        self.connected = False
                
                if self.connected:
                    logger.info("Successfully connected to Chessnut Pro board")
                    try:
                        self.board_state = self.easylink.get_board_state()
                        
                        # Start the event listener thread
                        if self.listener_thread and self.listener_thread.is_alive():
                            logger.debug("Listener thread already running")
                        else:
                            self.listener_thread = threading.Thread(target=self._event_listener)
                            self.listener_thread.daemon = True
                            self.listener_thread.start()
                    except Exception as e:
                        logger.error(f"Error initializing board state: {e}")
                        self.connected = False
                        self.last_error = str(e)
                        if self.error_callback:
                            self.error_callback(f"Error initializing board: {e}")
                else:
                    logger.warning("Failed to connect to Chessnut Pro board")
                    if self.error_callback:
                        self.error_callback("Failed to connect to Chessnut Pro")
                    
                    if auto_retry and self.connection_attempts < self.max_connection_attempts:
                        logger.info(f"Will retry connection in 5 seconds (attempt {self.connection_attempts}/{self.max_connection_attempts})...")
                        time.sleep(5)
                        # Try to reconnect (outside of lock to avoid deadlock)
        
        except Exception as e:
            logger.error(f"Error connecting to Chessnut Pro: {e}")
            self.last_error = str(e)
            if self.error_callback:
                self.error_callback(f"Connection error: {e}")
            self.connected = False
        
        # If we should retry and reached here (likely due to error), try again outside the lock
        if auto_retry and not self.connected and self.connection_attempts < self.max_connection_attempts:
            self._connect_thread(device_name, auto_retry)
    
    def ensure_connection(self):
        """
        Check connection and attempt to reconnect if disconnected
        
        Returns:
            True if connected, False otherwise
        """
        if not self.sdk_available:
            return False
            
        if not self.connected and self.auto_reconnect:
            logger.info("Connection lost. Attempting to reconnect...")
            # Reset connection attempts for a fresh reconnection cycle
            self.connection_attempts = 0
            return self.connect(auto_retry=True)
        return self.connected
    
    def _event_listener(self):
        """Thread function for listening to board events"""
        try:
            logger.info("Starting board event listener")
            
            # Register callback for board events
            if self.easylink:
                self.easylink.register_event_callback(self._board_event_callback)
                
                # Keep thread alive with a small enough interval to detect disconnections
                while self.running and self.connected:
                    time.sleep(0.1)
                    
                    # Periodically check if still connected (every 5 seconds)
                    if time.time() - self.last_sync_time > 5:
                        try:
                            if self.easylink:
                                # A lightweight operation to check connection
                                self.board_state = self.easylink.get_board_state()
                                self.last_sync_time = time.time()
                        except Exception as e:
                            logger.warning(f"Connection check failed: {e}")
                            self.connected = False
                            if self.error_callback:
                                self.error_callback("Lost connection to Chessnut Pro")
                            
                            # Try to reconnect if auto-reconnect is enabled
                            if self.auto_reconnect:
                                self.ensure_connection()
        
        except Exception as e:
            logger.error(f"Error in board event listener: {e}")
            self.last_error = str(e)
            if self.error_callback:
                self.error_callback(f"Board listener error: {e}")
            self.connected = False
    
    def _board_event_callback(self, event: BoardEvent):
        """Callback for board events from the Chessnut Pro"""
        try:
            if not event:
                return
                
            if hasattr(event, 'event_type') and event.event_type == "move":
                # A move was made on the physical board
                if not hasattr(event, 'move') or not event.move:
                    logger.warning("Received move event without move data")
                    return
                    
                move = event.move
                
                # Ensure the move has the required attributes
                if not hasattr(move, 'from_square') or not hasattr(move, 'to_square'):
                    logger.warning("Received incomplete move data")
                    return
                
                # Convert to UCI format (e.g., e2e4)
                uci_move = f"{move.from_square}{move.to_square}"
                
                # Special handling for castling
                if hasattr(move, 'piece') and move.piece and hasattr(move.piece, 'type') and move.piece.type == "king":
                    # Detect kingside castling (king moves two squares to the right)
                    if move.from_square[0] == 'e' and move.to_square[0] == 'g':
                        logger.info("Detected kingside castling")
                    # Detect queenside castling (king moves two squares to the left)
                    elif move.from_square[0] == 'e' and move.to_square[0] == 'c':
                        logger.info("Detected queenside castling")
                
                # Special handling for pawn promotion
                if hasattr(move, 'piece') and move.piece and hasattr(move.piece, 'type') and move.piece.type == "pawn":
                    if move.to_square[1] in ["1", "8"]:
                        # This is a pawn promotion
                        logger.info("Detected pawn promotion")
                        # The game will prompt for promotion piece later - no need to add it here
                
                logger.info(f"Move detected on board: {uci_move}")
                
                # Put the move in the queue
                self.move_queue.put(uci_move)
                
                # Call the move callback if set
                if self.move_callback:
                    self.move_callback(uci_move)
            
            elif hasattr(event, 'event_type') and event.event_type == "board_changed":
                # The board state changed (piece added/removed manually)
                if hasattr(event, 'board_state'):
                    self.board_state = event.board_state
                    logger.debug("Board state updated")
            
            elif hasattr(event, 'event_type') and event.event_type == "connection_lost":
                # Connection to the board was lost
                logger.warning("Connection to Chessnut Pro was lost")
                self.connected = False
                if self.error_callback:
                    self.error_callback("Connection to Chessnut Pro was lost")
                
                # Try to reconnect if auto-reconnect is enabled
                if self.auto_reconnect:
                    self.ensure_connection()
        
        except Exception as e:
            logger.error(f"Error processing board event: {e}")
            self.last_error = str(e)
            if self.error_callback:
                self.error_callback(f"Board event error: {e}")
    
    def get_move(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Get the next move from the physical board
        
        Args:
            timeout: How long to wait for a move (seconds), or None to return immediately
        
        Returns:
            The move in UCI format (e.g., e2e4) or None if no move is available
        """
        try:
            # Check connection first
            if not self.ensure_connection():
                return None
                
            return self.move_queue.get(block=timeout is not None, timeout=timeout)
        except queue.Empty:
            return None
        except Exception as e:
            logger.error(f"Error getting move: {e}")
            return None
    
    def set_board_to_match_position(self, board) -> bool:
        """
        Synchronize physical board with game state
        
        Args:
            board: Chess board object with current game state
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.ensure_connection():
                return False
                
            fen = board.fen()
            logger.info(f"Synchronizing board to position: {fen}")
            self.easylink.set_position(fen)
            self.last_sync_time = time.time()
            return True
        except Exception as e:
            logger.error(f"Failed to sync board state: {e}")
            self.last_error = str(e)
            if self.error_callback:
                self.error_callback(f"Failed to sync board: {e}")
            return False
    
    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get detailed connection status
        
        Returns:
            Dictionary with connection status details
        """
        return {
            "connected": self.connected,
            "sdk_available": self.sdk_available,
            "last_error": self.last_error,
            "connection_attempts": self.connection_attempts,
            "auto_reconnect": self.auto_reconnect
        }
    
    def disconnect(self):
        """Disconnect from the Chessnut Pro board"""
        logger.info("Disconnecting from Chessnut Pro")
        self.running = False
        
        with self.connection_lock:
            if self.connected and self.easylink:
                try:
                    self.easylink.disconnect()
                    logger.info("Successfully disconnected from Chessnut Pro")
                except Exception as e:
                    logger.error(f"Error disconnecting from Chessnut Pro: {e}")
                finally:
                    self.connected = False
                    self.easylink = None


# Integration with chess module
def integrate_with_chess_manager(chess_match_manager):
    """
    Integrates the Chessnut Pro with the game's chess match manager
    
    Args:
        chess_match_manager: The chess match manager from the game
    
    Returns:
        The modified chess_match_manager
    """
    if not EASYLINK_AVAILABLE:
        logger.warning("EasyLinkSDK not available. Chessnut integration disabled.")
        # Store a dummy interface so the rest of the code can still reference it
        chess_match_manager.chessnut = ChessnutInterface()
        return chess_match_manager
    
    original_get_player_move = chess_match_manager.get_player_move
    original_play_match = chess_match_manager.play_match
    chessnut = ChessnutInterface()
    
    def move_callback(move):
        logger.info(f"Move detected on Chessnut board: {move}")
    
    def error_callback(error):
        logger.warning(f"Chessnut error: {error}")
    
    chessnut.set_callbacks(move_callback, error_callback)
    
    # Attempt to connect to the board
    connected = chessnut.connect(auto_retry=True)
    
    # Store the interface in the manager for access elsewhere
    chess_match_manager.chessnut = chessnut
    
    # Replace the get_player_move method to check for physical moves
    def enhanced_get_player_move(board):
        """Enhanced get_player_move that checks for physical moves"""
        if chessnut.connected:
            print("Waiting for move on Chessnut Pro board or enter move manually...")
            
            # Try to get a move from the board (with a small timeout)
            physical_move = chessnut.get_move(timeout=0.1)
            if physical_move:
                print(f"Move detected on physical board: {physical_move}")
                try:
                    # For pawn promotion, we need to handle it specially
                    if len(physical_move) == 4:  # Standard move
                        from_square = physical_move[:2]
                        to_square = physical_move[2:4]
                        
                        # Check if this is a potential promotion
                        piece = board.piece_at(chess.parse_square(from_square))
                        if piece and piece.piece_type == chess.PAWN:
                            # Check if moving to the last rank
                            if (piece.color == chess.WHITE and to_square[1] == '8') or \
                               (piece.color == chess.BLACK and to_square[1] == '1'):
                                # Ask user what piece to promote to
                                promotion_piece = None
                                while promotion_piece not in ['q', 'r', 'b', 'n']:
                                    promotion_piece = input("Promote to (q)ueen, (r)ook, (b)ishop, or k(n)ight? ").lower()
                                    if promotion_piece not in ['q', 'r', 'b', 'n']:
                                        print("Invalid choice. Please enter q, r, b, or n.")
                                
                                # Add promotion piece to the move
                                physical_move += promotion_piece
                    
                    move = chess.Move.from_uci(physical_move)
                    if move in board.legal_moves:
                        return move
                    else:
                        print("Illegal move detected on physical board. Please make a valid move.")
                except ValueError as ve:
                    print(f"Invalid move format from physical board: {ve}. Please try again.")
                except Exception as e:
                    print(f"Error processing move: {e}. Please try again.")
        
        # Fall back to the original method if no valid move from the board
        return original_get_player_move(board)
    
    # Override the original get_player_move method
    chess_match_manager.get_player_move = enhanced_get_player_move
    
    # Enhance play_match to better sync the physical board
    def enhanced_play_match(opponent_name, opponent_elo, time_control="90/30"):
        """Enhanced play_match that syncs the physical board"""
        # Initialize the board
        board = chess.Board()
        
        # Set up engine strength
        if chess_match_manager.engine:
            chess_match_manager.set_engine_strength(opponent_elo)
        
        # Set initial board position on Chessnut if connected
        if chessnut.connected:
            print("Synchronizing your Chessnut Pro board...")
            if chessnut.set_board_to_match_position(board):
                print("Board synchronized. Make sure pieces are in the starting position.")
            else:
                print("Failed to synchronize board. Please set up the starting position manually.")
        
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
        chess_match_manager.display_match_intro(opponent_name, opponent_elo, time_control)
        
        # Main game loop
        while not board.is_game_over():
            # Display the board
            chess_match_manager.display_board(board)
            
            # Display remaining time if using a clock
            if time_control:
                chess_match_manager.display_clock(player_time, engine_time)
            
            # Player's turn (white)
            if board.turn == chess.WHITE:
                start_time = time.time()
                
                move = chess_match_manager.get_player_move(board)
                
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
                
                if chess_match_manager.engine:
                    # Limit engine thinking time based on its remaining clock
                    time_limit = min(30, engine_time / 10) if time_control else 1.0
                    result = chess_match_manager.engine.play(board, chess.engine.Limit(time=time_limit))
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
                
                # Display the move and prompt the user to update their physical board
                move_uci = move.uci()
                print(f"\n{opponent_name} played: {move_uci}")
                
                # If physical board is connected, prompt user to update it
                if chessnut.connected:
                    print("Please make this move on your physical Chessnut board.")
                    input("Press Enter after updating your board...")
                    
                    # Try to verify board state is correct
                    chessnut.set_board_to_match_position(board)
                else:
                    time.sleep(1)  # Small pause for readability
        
        # Display final position
        chess_match_manager.display_board(board)
        
        # Determine and return the result
        return chess_match_manager.get_match_result(board)
    
    # Override the original play_match method
    chess_match_manager.play_match = enhanced_play_match
    
    return chess_match_manager
