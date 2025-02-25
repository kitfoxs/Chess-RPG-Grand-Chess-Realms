class LoreManager:
    """
    Manages the lore, story content, and narrative progression
    for the Grand Chess Realms game.
    """
    
    def __init__(self):
        # Initialize lore collections
        self.history = self.init_historical_lore()
        self.locations = self.init_location_lore()
        self.characters = self.init_character_lore()
        self.items = self.init_item_lore()
        self.quests = self.init_quest_storylines()
        self.books = self.init_in_game_books()
        
        # Track discovered lore
        self.discovered_lore = set()
    
    def init_historical_lore(self):
        """Initialize historical lore entries"""
        return {
            "creation_myth": {
                "title": "The First Game - Creation Myth",
                "content": """According to ancient myth, the world was born from a cosmic chess match between twin deities of Light and Shadow. It's said that each move they played shaped continents and creatures, crafting the balance of day and night across the land. This primordial "Game of Creation" established the eternal rivalry between the White and Black Kingdoms.

Some legends claim the gods taught mortals the game to resolve conflicts without bloodshed—an ancient practice echoing real-world tales where chess was invented as a less bloody equivalent to war."""
            },
            "two_kingdoms": {
                "title": "The Rise of Two Kingdoms",
                "content": """Human history in the Grand Chess Realms began with the rise of two great kingdoms, one under a banner of ivory (the White Kingdom) and the other under a standard of obsidian (the Black Kingdom).

The White Kingdom traces its lineage to King Aurelius the Radiant, a benevolent warrior-scholar who unified the western lands through fairness and skill at the chessboard as much as in battle.

To the east, the Black Kingdom was forged by Emperor Kaine the Shadowcaster, a cunning warlord-priest who rallied ambitious houses under a dark crown, proving his right to rule in strategic duels as much as open combat.

From the very beginning, their philosophies diverged: White cherished honor, light, and chivalry, while Black embraced ambition, secrecy, and pragmatism."""
            },
            "war_of_two_kings": {
                "title": "The War of the Two Kings",
                "content": """The first great war, known as The War of the Two Kings, erupted when neither Aurelius nor Kaine would yield a border fortress. This war raged on battlefields and in war councils that were essentially giant chess matches—generals moved real armies as if pieces on a board.

Historians describe commanders using an actual oversized chessboard map to simulate tactics, reflecting how chess was historically used to model warfare strategies.

The war ended in an uneasy Treaty of Stalemate, signed on neutral ground after both sides reached a deadlock."""
            },
            "gambit_of_queens": {
                "title": "The Gambit of Queens",
                "content": """Later came The Gambit of Queens, a conflict sparked when Queen Regana of the Black Kingdom and Queen Elissa of the White Kingdom personally took charge of their armies.

These rival queens proved as fearsome and brilliant as any king, ushering in an age where queens wielded unprecedented power—a shift paralleled by the rise of the queen piece's power in old chess history.

Their strategic genius led to innovations in both warfare and chess play, with several famous chess openings still bearing their names today."""
            },
            "grand_tournament": {
                "title": "The Grand Tournament of Strategy",
                "content": """During peacetime, a cultural renaissance bloomed in both kingdoms. Scholarly orders and knightly guilds formed, and chess became the heart of education and diplomacy.

A grand tradition was established where every five years a great chess tournament replaces open warfare. Rather than waste lives, champions from White and Black (and neutral lands) face off in the Grand Tournament of Strategy to settle disputes and honor the gods of the game.

This tradition has its roots in a legendary event: a dispute between two noble houses over a marriage was once settled by a live chess duel—two champions played on a field with soldiers as living pieces, witnessed by the entire realm. The outcome of that historic match shaped the lineages and inspired the idea that brain should triumph over brawn."""
            },
            "prophecy_checkmate": {
                "title": "The Prophecy of the Final Checkmate",
                "content": """Among the most famous prophecies is The Prophecy of the Final Checkmate, which claims that:

"When a player of neither white nor black achieves the ultimate checkmate, the eternal stalemate shall end and the realms reunite."

Scholars debate the meaning of this cryptic prophecy. Some believe it foretells the coming of a neutral champion who will unite the kingdoms. Others interpret it as a warning about a third power rising to conquer both kingdoms.

Many adventurers and chess masters seek to understand and possibly fulfill this prophecy, each with their own interpretation of what the "ultimate checkmate" might be."""
            }
        }
    
    def init_location_lore(self):
        """Initialize location-specific lore"""
        return {
            "white_kingdom": {
                "title": "The White Kingdom (Albion)",
                "content": """The White Kingdom, often simply called Albion, spans fertile plains, rolling hills, and shining cities of marble and limestone.

Its capital is Castle Lumina, a fortress-city of white stone that gleams at sunrise. Castle Lumina's central keep is known as the Ivory Tower, where the White King's throne room floor is a massive mosaic chessboard.

In the great hall, courtiers play at giant chess sets while discussing matters of state. The city is also home to the Grand Cathedral of Dawn, seat of the High Bishop of Light. Pilgrims travel here to witness daily chess matches played by robed clerics as a form of ritual—a practice that reaffirms the realm's faith that strategy and piety go hand in hand."""
            },
            "black_kingdom": {
                "title": "The Black Kingdom (Noir)",
                "content": """The Black Kingdom, known in old lore as Noir, covers dark forests, rugged mountains, and cities built of basalt and obsidian.

Its capital city is Ebonhold, centered around the Obsidian Fortress—a colossal black-stone castle whose spires are shaped like pointed black chess pieces against the sky.

Beneath Ebonhold lies the Catacomb of Shadows, where the Shadow Cult performs rites and where generations of Black kings have been laid to rest. In the grand throne room of the Black Castle, the floor is also a checkered board, but inlaid with black marble and bloodstone; here the Black King is said to play against his advisors on an elaborate onyx and ivory set when deliberating war, believing that each move contemplates a course of action."""
            },
            "checkered_frontier": {
                "title": "The Checkered Frontier",
                "content": """Between Albion and Noir lie contested lands often called The Checkered Frontier or Middle Board by common folk. These rolling plains and ruined forts have changed hands many times, resulting in a patchwork of white and black banners over the years.

One prominent landmark here is the Field of Stalemate, a broad expanse where a titanic battle once ended with neither side victorious. To this day, the field remains dotted with petrified remains of warriors and knights, as if the gods themselves declared a draw and froze the conflict in time.

Travelers say on certain nights, ghostly figures (the spirits of fallen pawns and knights) reenact their final moves across the field under the moonlight."""
            },
            "white_village": {
                "title": "The White Village",
                "content": """The White Village is a small but picturesque settlement under the protection of the White Kingdom. Cottages with thatched roofs and whitewashed walls cluster around a central square paved with alternating light and dark stones in a checkered pattern.

Every morning, villagers gather here to trade goods, share news, and play casual games of chess on stone tables permanently set up for this purpose. The village is known for its annual chess tournament, where the winner receives a wreath of white flowers and the honorary title "Village Champion" for the year.

The village's economy centers around farming and crafting, with several artisans specializing in carving wooden chess sets. Their White Village chess sets are prized throughout the kingdom for their detailed craftsmanship."""
            },
            "hermits_clearing": {
                "title": "The Hermit's Clearing",
                "content": """Deep in the forest lies a peaceful clearing where Elowen the Hermit has made her home. Her modest hut is decorated with chess symbols and surrounded by a garden of both medicinal and culinary herbs arranged in a pattern reminiscent of a chessboard.

A stone table with a chessboard carved into its surface stands under an ancient oak tree. The pieces, carved from polished wood, show signs of frequent use.

Legend says that Elowen was once a prodigy at the White court who withdrew from society after a personal tragedy. Some claim she achieved an enlightenment through chess that gave her prophetic abilities.

Those seeking wisdom must undertake seven trials—symbolic of a pawn's journey across the board—before Elowen will share her insights."""
            },
            "crossroads": {
                "title": "The Crossroads",
                "content": """The Crossroads marks a significant junction where several paths converge. A weathered stone marker stands at the center, inscribed with directions to key locations in both kingdoms.

This area is considered neutral ground, and travelers from both White and Black kingdoms pass through regularly. A small waystation provides basic amenities to weary travelers, and it's common to see impromptu chess matches between strangers of different allegiances here.

The Crossroads is also home to a curious tradition: travelers often leave a small token or chess piece at the base of the marker for good fortune, creating a constantly changing collection of mementos from across the realms."""
            }
        }
    
    def init_character_lore(self):
        """Initialize character lore"""
        return {
            "king_lucan": {
                "title": "King Lucan IV \"the Ivory King\"",
                "content": """The current ruling monarch of Albion, King Lucan is a direct descendant of Aurelius. Now in his early fifties, Lucan is known for just rule and strategic mind.

He was schooled in chess and statecraft from childhood, and it's said he can play three games simultaneously while conducting a council meeting. A kindly ruler, he strives for peace but will not shy from war if provoked.

In battle, he leads from the front like a king on the board—protected but pivotal. Many credit King Lucan's careful maneuvers, both political and military, for maintaining the Treaty of Stalemate these last two decades.

He often quotes old proverbs during court sessions, such as "Protect the King at all costs," reminding those around him that the welfare of the realm (the king's safety) is paramount."""
            },
            "emperor_darius": {
                "title": "Emperor Darius Blackbourne",
                "content": """The ruler of Noir, often referred to simply as the Black King (though he styles himself Emperor), Darius is a formidable figure feared and respected in equal measure.

He inherited the throne young after a series of mysterious deaths in his family and has ruled with shrewd efficiency. Emperor Darius is a master of psychological strategy—he's been known to deliberately lose unimportant chess games to lull opponents into underestimating him, only to outmaneuver them later in politics or war.

Under his reign, the Black Kingdom has fortified its defenses and expanded influence subtly through vassals and proxies rather than outright conquest.

He keeps a set of ravens (his emblem) and purportedly consults them like an augury when making decisions, comparing their movements to pieces on a mental board."""
            },
            "sir_galwynne": {
                "title": "The Wandering Arbiter, Sir Galwynne",
                "content": """A knight-errant turned neutral peacekeeper, Sir Galwynne is a silver-haired veteran who has renounced allegiance to either kingdom to serve a higher cause: balance.

Bearing a tunic with a grey chess knight symbol, he travels the land mediating conflicts and enforcing the ancient codes of honorable play. Galwynne was once a celebrated White Knight, but after witnessing the horrors of war, he pledged himself to the service of the cosmic Balance (some say he had a vision from the Twin Chess Gods to keep the scales even).

He carries a traveling chessboard inscribed with magical runes. When two parties are at odds, he compels them to play out their dispute on this board under his arbitration.

Many brigands and hotheaded lords have grudgingly respected this ritual, for Galwynne's reputation and mastery of combat are formidable if anyone refuses the civilized route."""
            },
            "elowen": {
                "title": "Elowen the Hermit of the 8th Rank",
                "content": """In the remote highlands, an eccentric hermit named Elowen dwells in a modest hut marked with carved chess symbols. Elowen is a former academic from Albion who many years ago withdrew from society after a personal tragedy.

She is known as the Hermit of the 8th Rank because those who seek her wisdom must undertake a symbolic journey "across the board"—traversing seven difficult trials in the wild (which she may or may not be subtly orchestrating) to prove their commitment. If they succeed, reaching her abode represents the pawn's promotion to the eighth rank.

Elowen possesses encyclopedic knowledge of opening strategies, herb lore, and ancient myths. She claims that through solitude and meditation on chess problems, she has learned to hear the "music of the squares"—cryptic phrases that hint she might possess magical or prophetic abilities.

Despite her seclusion, she is surprisingly up-to-date on world events, often startling visitors by knowing about events that happened just days prior. Some say forest spirits or wandering birds carry news to her."""
            },
            "rowan": {
                "title": "Rowan the Black Bandit",
                "content": """A notorious chess hustler and minor villain, Rowan travels from village to village challenging locals to chess matches with wagers attached. His black clothing and intimidating demeanor have earned him the nickname "Black Bandit," though he has no official connection to the Black Kingdom.

Rumor has it that Rowan was once a promising student at a prestigious chess academy but was expelled for cheating. Now he uses his considerable skills to prey on less experienced players, especially in remote villages where advanced chess training is rare.

He carries a fine chess set with pieces allegedly taken as trophies from his victories. Despite his villainous reputation, Rowan follows a strict code: he never forces anyone to play, and he always honors the outcome of a match, win or lose."""
            },
            "elder_thomas": {
                "title": "Elder Thomas",
                "content": """The respected leader of the White Village, Elder Thomas has governed with wisdom and fairness for decades. His long white beard and calm demeanor give him an air of authority, while his kind eyes reflect his genuine care for the villagers.

In his youth, Thomas served as a diplomat for the White Kingdom, traveling extensively and learning various regional chess styles. He returned to his home village after retiring from court service, bringing with him knowledge and connections that have helped the village prosper.

Thomas is a patient teacher who spends his evenings instructing the village youth in both chess and ethics, believing that the principles of the game—foresight, sacrifice, and protection—translate directly to virtuous living.

Recently, Thomas has grown concerned about Rowan the Black Bandit, who has been challenging villagers to unfair matches and taking their prized possessions."""
            }
        }
    
    def init_item_lore(self):
        """Initialize item lore"""
        return {
            "basic_chess_set": {
                "title": "Basic Chess Set",
                "content": """A simple wooden chess set with hand-carved pieces. Though modest in appearance, it's well-crafted and durable, suitable for travel. The pieces have a pleasing weight in the hand, and the board folds in half for easy storage.

This particular style of chess set is common throughout the White Kingdom, often crafted by village artisans as part of their coming-of-age training. The White Village is particularly known for the quality of their basic sets."""
            },
            "lore_book_white_kingdom": {
                "title": "Chronicles of the White Kingdom",
                "content": """A leather-bound tome with the White Kingdom's emblem embossed on the cover. The pages contain histories, myths, and legends of Albion, carefully recorded by royal historians.

The book includes accounts of the founding of the White Kingdom under King Aurelius, major historical battles, and the evolution of chess traditions within the realm. Particularly noteworthy are the illustrated pages depicting famous chess matches that decided the outcomes of wars or succession disputes.

Reading this book provides valuable insight into White Kingdom culture and history, potentially useful for travelers navigating its territories."""
            },
            "mysterious_scroll": {
                "title": "Mysterious Scroll",
                "content": """A weathered parchment sealed with wax bearing the imprint of a chess piece—specifically, a knight. The scroll appears old, but the seal remains unbroken.

The exterior of the scroll bears no markings to indicate its contents or origin, though the quality of the parchment suggests it was created by someone of means or scholarly background.

Breaking the seal might reveal important information, but doing so irreversibly alters the artifact. Some collectors value sealed messages for their mystery and potential."""
            },
            "hermits_strategy": {
                "title": "The Hermit's Strategy",
                "content": """Not a physical item but rather a chess technique taught by Elowen the Hermit. This strategic approach focuses on patient development, unexpected sacrifices, and the power of seemingly minor pieces.

Those who learn the Hermit's Strategy gain insight into unconventional chess tactics that can confound opponents who rely on standard openings and responses. The strategy emphasizes the value of pawns and their potential for promotion—a philosophy that mirrors Elowen's belief in the hidden potential within seemingly ordinary people.

In gameplay terms, knowledge of this strategy might provide an advantage in certain chess matches or unlock dialogue options with chess enthusiasts encountered during travel."""
            },
            "victory_token": {
                "title": "Victory Token",
                "content": """A polished wooden disk with a chess piece carved on one side and the symbol of victory—a laurel wreath—on the other. These tokens are traditionally awarded to winners of official chess matches and tournaments throughout the realms.

Beyond their commemorative value, victory tokens serve as proof of skill and can sometimes grant access to exclusive chess clubs, master-level training, or special events. Some establishments offer discounts or special treatment to those who can produce a victory token, recognizing them as accomplished strategists.

Collecting victory tokens from various regions or defeating notable opponents can enhance a player's reputation in chess circles."""
            }
        }
    
    def init_quest_storylines(self):
        """Initialize quest storylines"""
        return {
            "defeat_village_champion": {
                "title": "The Village Champion's Challenge",
                "description": "The White Village has been troubled by Rowan the Black Bandit, who challenges locals to chess matches and takes their prized possessions when they win. Elder Thomas has asked you to confront him and put an end to his schemes.",
                "objectives": [
                    "Find and challenge Rowan in the Town Square",
                    "Defeat him in a chess match",
                    "Return to Elder Thomas"
                ],
                "reward": "Victory Token and the gratitude of the village",
                "story_progression": [
                    "Upon accepting the quest, several villagers approach you with stories about Rowan's tactics and the items they've lost.",
                    "When you confront Rowan, he's initially dismissive but agrees to a match when you demonstrate your determination.",
                    "During the match, a crowd gathers to watch, creating a tense atmosphere.",
                    "If you win, Rowan reluctantly returns the villagers' possessions and leaves, promising to seek more worthy opponents elsewhere.",
                    "Elder Thomas holds a small celebration in your honor, presenting you with a Victory Token and naming you an honorary protector of the village."
                ]
            },
            "hermit_training": {
                "title": "The Hermit's Wisdom",
                "description": "Rumors speak of a hermit in the forest who possesses ancient chess knowledge. Seeking her out could grant you valuable strategic insights.",
                "objectives": [
                    "Find the Hermit's Clearing in the forest",
                    "Prove your worth to Elowen through a chess match",
                    "Complete her training"
                ],
                "reward": "The Hermit's Strategy",
                "story_progression": [
                    "When you reach the Hermit's Clearing, Elowen initially seems reluctant to teach you.",
                    "She challenges you to a chess match not to test your skill but your approach to the game.",
                    "Win or lose, if you demonstrate thoughtfulness and respect for the game, she agrees to share her knowledge.",
                    "Elowen's training involves unusual exercises: playing blindfolded, with pieces arranged in seemingly impossible positions, or with unorthodox rules.",
                    "After completing her training, you gain insight into her unique approach to chess, which may prove advantageous in future matches."
                ]
            },
            "knight_challenge": {
                "title": "The Wandering Knight's Test",
                "description": "Sir Galwynne, a neutral knight who serves as an arbiter between the kingdoms, is looking for worthy champions to help maintain balance in the realm.",
                "objectives": [
                    "Meet Sir Galwynne at the Crossroads",
                    "Engage in his test of character and chess skill",
                    "Demonstrate your commitment to honor and strategy"
                ],
                "reward": "Sir Galwynne's Recommendation and a special chess piece",
                "story_progression": [
                    "When you meet Sir Galwynne, he explains that the realms need individuals who understand that chess is more than a game—it's a framework for resolving conflicts peacefully.",
                    "His test involves both a chess match and ethical scenarios where you must decide how to apply the principles of chess to real-world dilemmas.",
                    "The outcome isn't determined solely by whether you win the match but by how you approach both challenges.",
                    "If you demonstrate both skill and principle, Sir Galwynne presents you with a knight piece from his personal chess set and a letter of recommendation.",
                    "This recommendation can open doors in both kingdoms and neutral territories, as Sir Galwynne is respected across the realm for his impartiality."
                ]
            }
        }
    
    def init_in_game_books(self):
        """Initialize contents for in-game books and scrolls"""
        return {
            "chronicles_white_kingdom": {
                "title": "Chronicles of the White Kingdom",
                "author": "Royal Historian Bertram",
                "content": """[Chapter 1: The Dawn of Albion]

In the first age, when the world was young and the cosmic chess match between Light and Shadow had barely begun, there arose in the western lands a great leader named Aurelius. Skilled in both the art of war and the game of kings, Aurelius united the scattered settlements under a single banner—a white castle on a field of silver.

The Kingdom of Albion, as it came to be known, was founded on principles of honor, order, and strategic wisdom. Aurelius decreed that disputes among his lords would be settled not by bloodshed but by matches of chess, thereby preserving the strength of the realm for external threats.

In those early days, the kingdom faced many challenges. Barbaric tribes from the northern wastes, creatures of shadow from the eastern mountains, and internal strife all threatened the young nation. Yet through careful planning—moving his forces like pieces on a board—Aurelius preserved and expanded his domain.

[Chapter 2: The First Conflict with Noir]

It was during the reign of Aurelius's grandson, King Cedric the Wise, that the eastern power of Noir first made itself known to Albion. Where Albion valued openness, honor, and direct approaches, Noir cultivated secrecy, ambition, and indirect strategies.

The first conflict came not over territory or resources but over ideology. Emperor Kaine of Noir sent envoys proposing an alliance, but with terms that would have required Albion to adopt many of Noir's practices. King Cedric, after careful consideration of the proposal as he would a chess position, declined.

Tensions escalated until the two powers met at what is now called the Field of First Contact. Rather than commit their armies to battle, Cedric challenged Kaine to a chess match to resolve their differences. The match lasted three days and ended in a draw—a result that established the pattern of stalemate between the two realms that persists to this day.

[Chapter 3: The Codification of Chess in Albion]

As Albion grew and flourished, the game of chess evolved from a simple contest into an integral part of society. During the reign of Queen Elissa, the kingdom's greatest scholars gathered to standardize the rules and record the most effective strategies.

The resulting tome, "The White Compendium," established not only the formal rules of chess as played in Albion but also connected the game to the kingdom's values and governance. The movement of pieces was tied to the roles of different social classes, with the following principles established:

1. The King's safety is paramount, just as the realm's stability depends on consistent leadership.
2. The Queen's versatility represents the adaptability needed to protect the kingdom.
3. Bishops move diagonally, representing how faith and wisdom often approach problems indirectly.
4. Knights move in L-shapes, showing how courage and martial skill can overcome obstacles in unexpected ways.
5. Rooks move in straight lines, embodying the direct protection offered by castle walls and loyal defenders.
6. Pawns advance steadily forward, demonstrating how even the common folk can achieve greatness through perseverance.

These principles became the foundation of Albion's approach to both chess and governance."""
            },
            "mysteries_of_the_checkered_fate": {
                "title": "Mysteries of the Checkered Fate",
                "author": "Unknown Sage",
                "content": """[On the Origin of the Prophecy]

The Prophecy of the Final Checkmate first appeared in the writings of the sage Morvaine, who lived during the Great Stalemate that followed the War of Two Kings. Morvaine claimed to have received the prophecy in a dream where the twin chess deities played on a board that encompassed the entire world.

According to historical accounts, Morvaine awoke from this dream and immediately transcribed these words:

"When a player of neither white nor black achieves the ultimate checkmate, the eternal stalemate shall end and the realms reunite."

Morvaine spent the remainder of his life attempting to interpret this vision, eventually establishing the Order of the Central Square, a philosophical society dedicated to studying the prophecy's meaning.

[Competing Interpretations]

Over the centuries, many interpretations of the prophecy have emerged:

The Unification Theory: Scholars of this school believe the prophecy foretells the rise of a neutral faction that will bring the White and Black Kingdoms together peacefully. They point to the phrase "reunite" as evidence that the kingdoms were once a single entity and are destined to become so again.

The Conquest Theory: A darker interpretation suggests that "a player of neither white nor black" refers to an outside force that will subjugate both kingdoms. Proponents note that "ultimate checkmate" implies a final, decisive victory rather than a negotiated peace.

The Transcendence Theory: Mystics and philosophers propose that the prophecy speaks not of political change but spiritual awakening. In this view, the "player" represents an enlightened consciousness that transcends duality, and the "ultimate checkmate" is the resolution of cosmic opposition.

The Literal Theory: Some chess masters suggest the prophecy simply predicts a revolutionary new approach to chess itself—perhaps a grandmaster who develops strategies beyond traditional white and black paradigms.

[Signs and Portents]

Those who study the prophecy closely watch for these signs that may indicate its fulfillment is near:

1. The appearance of chess pieces made of materials other than black or white
2. The birth of children with eyes of different colors (one black, one white)
3. The formation of new political entities that reject allegiance to either kingdom
4. The discovery of ancient chess sets with unusual properties or additional pieces
5. The emergence of players who consistently achieve draws against the greatest masters of both kingdoms

Whether one believes in the prophecy or dismisses it as superstition, its influence on the culture and politics of the Grand Chess Realms cannot be denied."""
            },
            "the_living_pieces": {
                "title": "The Living Pieces: Chess Creatures of the Realm",
                "author": "Archmage Thalen",
                "content": """[Introduction: Chess Beyond the Board]

The deep connection between chess and the fabric of our world has manifested in curious and sometimes dangerous ways. Throughout the Grand Chess Realms, creatures and constructs embodying the essence of chess pieces have been documented by explorers, scholars, and survivors.

This compendium serves as both a scholarly record and a practical guide for travelers who may encounter these entities in their journeys.

[Marble Sentinels]

Perhaps the most famous chess constructs are the Marble Sentinels that guard the White Kingdom's Ivory Tower. These 32 life-sized statues (16 white, 16 black) normally stand as decorative elements along the hallways but animate when the castle is threatened.

Witnesses report that these sentinels move with perfect coordination, as if directed by a single brilliant mind. They form battle formations identical to chess openings: pawns create a defensive line, knights leap forward to engage threats, bishops guard the flanks with magical projectiles, rooks secure key chokepoints, while the king and queen statues protect the central keep.

What makes these constructs particularly formidable is their adherence to chess movement patterns combined with their stone construction. A rook sentinel, for instance, can only move in straight lines but does so with unstoppable momentum, crushing anything in its path.

[Chess Golems]

Beyond full sets, individual Chess Golems are known to guard ancient sites and strategic locations. The most common variants include:

Rook Golems: Tower-shaped constructs that slide with tremendous force in straight lines. Their limitation to orthogonal movement has saved many clever adventurers who realized they could evade pursuit by moving diagonally.

Knight Automata: Clockwork knights that move in L-shaped patterns, making their movements highly unpredictable. Their ability to "jump" over obstacles makes them effective in cluttered environments.

Bishop Sentinels: Floating constructs often used to patrol libraries and archives. They move exclusively along diagonal paths, often carrying magical lights that illuminate dark corners.

Queen's Guardians: The rarest and most dangerous constructs, capable of movement in any direction. These are typically reserved for protecting the most valuable treasures or important personages.

[Enchanted Beasts]

Some natural creatures have been magically altered to embody chess principles:

Knightmares: Jet-black horses with manes of starlight that can teleport in L-shaped patterns over short distances. Originally bred for elite cavalry units, some have escaped and formed wild herds in remote areas.

Ravenous Rooks: Strange creatures that camouflage themselves as crumbling towers. When prey approaches, they unfold into massive stone birds that attack with devastating straight-line charges.

Bishop Wolves: Pack predators with diagonal striping that hunt exclusively along diagonal paths through forests. They possess unusual intelligence and are known to coordinate their movements to corner prey.

[Encountering Chess Creatures]

If you encounter these entities, remember these principles:

1. Chess constructs are bound by their movement patterns. Positioning yourself where they cannot legally move often renders you safe.

2. Many constructs respond to chess notation commands if spoken with authority. The phrase "e2e4" might compel a pawn construct to move accordingly.

3. Chess creatures often cannot cross boundaries that resemble board edges. Drawing a checkered pattern on the ground has been known to confuse or contain them.

4. Most importantly, remember that these are not mindless automatons but entities with an intrinsic understanding of strategy. What seems like a safe position may be part of their longer tactical plan."""
            }
        }
    
    def get_lore_entry(self, category, entry_id):
        """Retrieve a specific lore entry"""
        if category == "history":
            collection = self.history
        elif category == "locations":
            collection = self.locations
        elif category == "characters":
            collection = self.characters
        elif category == "items":
            collection = self.items
        elif category == "books":
            collection = self.books
        else:
            return None
            
        if entry_id in collection:
            # Mark as discovered
            self.discovered_lore.add(f"{category}:{entry_id}")
            return collection[entry_id]
        return None
    
    def get_book_content(self, book_id):
        """Get the content of an in-game book"""
        if book_id in self.books:
            book = self.books[book_id]
            # Mark as discovered
            self.discovered_lore.add(f"books:{book_id}")
            return book
        return None
    
    def get_quest_info(self, quest_id):
        """Get information about a specific quest"""
        if quest_id in self.quests:
            return self.quests[quest_id]
        return None
    
    def get_random_lore(self, category=None):
        """Get a random lore entry, optionally from a specific category"""
        if category == "history":
            collection = self.history
        elif category == "locations":
            collection = self.locations
        elif category == "characters":
            collection = self.characters
        elif category == "items":
            collection = self.items
        elif category == "books":
            return random.choice(list(self.books.values()))
        else:
            # Choose a random category if none specified
            collections = [self.history, self.locations, self.characters, self.items]
            collection = random.choice(collections)
        
        # Select a random entry from the chosen collection
        entry_id = random.choice(list(collection.keys()))
        
        # Mark as discovered
        self.discovered_lore.add(f"{category}:{entry_id}")
        
        return collection[entry_id]
    
    def get_location_description(self, location_id):
        """Get a rich description for a location, including relevant lore"""
        # This would typically be called when a player enters a new area
        if location_id in self.locations:
            return self.locations[location_id]["content"]
        return None
    
    def get_character_background(self, character_id):
        """Get background information about a character"""
        if character_id in self.characters:
            return self.characters[character_id]["content"]
        return None
    
    def get_discovered_lore_count(self):
        """Return the number of lore entries discovered"""
        return len(self.discovered_lore)
    
    def is_lore_discovered(self, category, entry_id):
        """Check if a specific lore entry has been discovered"""
        return f"{category}:{entry_id}" in self.discovered_lore


# Sample usage of the LoreManager:
# 
# lore = LoreManager()
# 
# # Get specific lore
# creation_myth = lore.get_lore_entry("history", "creation_myth")
# print(creation_myth["title"])
# print(creation_myth["content"])
# 
# # Get a random piece of lore
# random_lore = lore.get_random_lore()
# print(random_lore["title"])
# print(random_lore["content"])
# 
# # Get book content
# book = lore.get_book_content("chronicles_white_kingdom")
# print(f"{book['title']} by {book['author']}")
# print(book["content"])


# Story Events Manager for Implementing Storylines
class StoryManager:
    """
    Manages story progression, events, and branching narratives
    for the Grand Chess Realms.
    """
    
    def __init__(self, game_instance, lore_manager):
        self.game = game_instance
        self.lore = lore_manager
        
        # Track story progression
        self.story_flags = {
            "intro_complete": False,
            "met_elder_thomas": False,
            "challenged_rowan": False,
            "defeated_rowan": False,
            "met_hermit": False,
            "completed_hermit_training": False,
            "met_wandering_knight": False,
            "aligned_white": False,
            "aligned_black": False,
            "aligned_neutral": False,
            "discovered_prophecy": False
        }
        
        # Story chapters/acts
        self.current_chapter = "chapter1"
        self.chapters = {
            "chapter1": "The White Village",
            "chapter2": "The Hermit's Wisdom",
            "chapter3": "The Crossroads",
            "chapter4": "The Checkered Frontier"
        }
        
        # Track completed events
        self.completed_events = []
    
    def trigger_story_event(self, event_id, parameters=None):
        """Trigger a story event based on ID"""
        # Prevent repeating events unless they're repeatable
        if event_id in self.completed_events and event_id not in ["random_encounter", "chess_tip"]:
            return False
        
        # Dictionary of event handlers
        event_handlers = {
            "intro_village": self.event_intro_village,
            "elder_thomas_meeting": self.event_elder_thomas_meeting,
            "challenge_rowan": self.event_challenge_rowan,
            "rowan_aftermath": self.event_rowan_aftermath,
            "discover_hermit": self.event_discover_hermit,
            "hermit_training": self.event_hermit_training,
            "meet_wandering_knight": self.event_meet_wandering_knight,
            "alignment_choice": self.event_alignment_choice,
            "discover_prophecy": self.event_discover_prophecy,
            "chapter_transition": self.event_chapter_transition,
            "random_encounter": self.event_random_encounter,
            "chess_tip": self.event_chess_tip
        }
        
        # Execute the event if it exists
        if event_id in event_handlers:
            result = event_handlers[event_id](parameters)
            
            # Mark event as completed if it was successful
            if result and event_id not in ["random_encounter", "chess_tip"]:
                self.completed_events.append(event_id)
            
            return result
        
        return False
    
    def check_story_triggers(self, location_id, action=None):
        """
        Check if any story events should be triggered based on
        location, actions, and current story state
        """
        # This would be called regularly to see if story events should trigger
        
        # Example triggers
        if location_id == "white_village" and not self.story_flags["intro_complete"]:
            self.trigger_story_event("intro_village")
        
        elif location_id == "elders_house" and not self.story_flags["met_elder_thomas"]:
            self.trigger_story_event("elder_thomas_meeting")
        
        elif location_id == "town_square" and self.story_flags["met_elder_thomas"] and not self.story_flags["challenged_rowan"]:
            # Only suggest the challenge, don't force it
            self.trigger_story_event("challenge_rowan")
        
        elif location_id == "town_square" and self.story_flags["challenged_rowan"] and not self.story_flags["rowan_aftermath"]:
            self.trigger_story_event("rowan_aftermath")
        
        elif location_id == "hermits_clearing" and not self.story_flags["met_hermit"]:
            self.trigger_story_event("discover_hermit")
        
        elif location_id == "crossroads" and not self.story_flags["met_wandering_knight"]:
            self.trigger_story_event("meet_wandering_knight")
    
    # Event handler methods
    def event_intro_village(self, parameters=None):
        """Introduction to the White Village"""
        self.display_story_text([
            "As you enter the White Village, you're struck by its quaint charm.",
            "Cottages with thatched roofs surround a central square where villagers gather around stone chess tables.",
            "The sound of chess pieces clicking against boards fills the air, along with animated discussions about strategies and recent matches.",
            "Children play with wooden pawns, mimicking the serious games their elders engage in.",
            "This is clearly a place where chess is not merely a pastime but a cornerstone of daily life."
        ])
        
        self.story_flags["intro_complete"] = True
        return True
    
    def event_elder_thomas_meeting(self, parameters=None):
        """Meeting with Elder Thomas"""
        self.display_story_text([
            "Elder Thomas looks up from a chess book as you enter his modest home.",
            "\"Ah, a new face in our village,\" he says with a welcoming smile.",
            "\"You've arrived at a troubled time, I'm afraid. A chess hustler calling himself 'The Black Bandit' has been challenging our villagers and taking their prized possessions when they lose.\"",
            "He gestures to a beautiful ivory chess set on the table.",
            "\"Chess is sacred to us—a way to resolve conflicts without bloodshed. This Rowan fellow has twisted that tradition for his own gain.\"",
            "Elder Thomas studies you with wise eyes.",
            "\"Perhaps you could help us? Rowan can usually be found in the town square, challenging passersby. If someone were to beat him at his own game, it might persuade him to leave our village in peace.\""
        ])
        
        self.story_flags["met_elder_thomas"] = True
        return True
    
    def event_challenge_rowan(self, parameters=None):
        """Suggesting the challenge against Rowan"""
        self.display_story_text([
            "As you enter the town square, you immediately spot a figure who must be Rowan the Black Bandit.",
            "Dressed in dark clothing with a confident smirk, he's setting up his chess pieces while a nervous-looking villager sits across from him.",
            "Several onlookers watch with worried expressions.",
            "Rowan looks up as you approach, his eyes quickly assessing you.",
            "\"Another potential victim?\" he chuckles. \"Or perhaps you're just here to watch this poor soul lose his grandfather's watch to me?\"",
            "The crowd murmurs. You sense this could be your opportunity to confront Rowan."
        ])
        
        self.story_flags["challenged_rowan"] = True
        return True
    
    def event_rowan_aftermath(self, parameters=None):
        """Aftermath of the Rowan challenge"""
        # Check if player won the challenge (would be stored in parameters)
        victory = parameters.get("victory", False) if parameters else False
        
        if victory:
            self.display_story_text([
                "The final move made, Rowan stares at the board in disbelief.",
                "\"Impossible,\" he mutters, then looks up at you with newfound respect.",
                "The crowd erupts in cheers as Rowan, true to his word despite his schemes, returns the items he won from the villagers.",
                "\"You play... differently,\" he admits. \"Perhaps there are still things for me to learn.\"",
                "Before departing, Rowan hesitates, then offers you his finest chess piece—a knight carved from obsidian.",
                "\"A token of respect,\" he says. \"May we meet again under different circumstances.\"",
                "As Rowan leaves the village, Elder Thomas approaches you with gratitude shining in his eyes.",
                "\"You've done us a great service today. The village is in your debt.\""
            ])
        else:
            self.display_story_text([
                "The match concluded, Rowan collects his winnings with a satisfied smile.",
                "\"Better luck next time,\" he says, not unkindly. \"You showed some promise, at least.\"",
                "The villagers disperse with disappointed murmurs. Elder Thomas approaches you with a sigh.",
                "\"You tried, and that's what matters. Rowan is exceptionally skilled—no one in the village has beaten him yet.\"",
                "He pats your shoulder encouragingly.",
                "\"Perhaps with more practice, or guidance from someone like the Hermit in the forest. There are always more matches to be played.\""
            ])
        
        self.story_flags["defeated_rowan"] = victory
        return True
    
    def event_discover_hermit(self, parameters=None):
        """Discovering the Hermit's clearing"""
        self.display_story_text([
            "The forest path opens into a serene clearing. At its center stands a modest hut surrounded by herb gardens laid out in a checkered pattern.",
            "An elderly woman sits at a stone table with a chessboard carved into its surface. She doesn't look up as you approach.",
            "\"Few find their way here without purpose,\" she says, moving a piece. \"Sit, if you wish.\"",
            "This must be Elowen, the hermit rumored to have once been a chess prodigy at the White court.",
            "The board before her contains a position unlike any you've seen—pieces arranged in a pattern that seems both beautiful and impossible.",
            "\"This puzzle has taken me three years to solve,\" she murmurs. \"The board speaks to those who truly listen.\""
        ])
        
        self.story_flags["met_hermit"] = True
        return True
    
    def event_hermit_training(self, parameters=None):
        """The Hermit's chess training"""
        self.display_story_text([
            "\"Training begins not with moving pieces, but understanding why they move as they do,\" Elowen explains.",
            "Over the course of several hours, she guides you through exercises that challenge conventional chess thinking:",
            "Playing blindfolded, to develop mental visualization...",
            "Solving positions where the objective is to lose all your pieces...",
            "Playing with the board rotated 45 degrees, changing your perception of the patterns...",
            "\"Chess is not about the pieces,\" she tells you. \"It's about the spaces between them, the tension, the potential.\"",
            "As dusk falls, Elowen finally nods with satisfaction.",
            "\"You've learned what I can teach in a day. The rest comes with reflection and practice.\"",
            "She presents you with a small wooden token carved with a chess pattern.",
            "\"This may help you see the board differently when you need it most.\""
        ])
        
        self.story_flags["completed_hermit_training"] = True
        # Add the hermit's strategy to player inventory
        if "hermits_strategy" not in self.game.player["inventory"]:
            self.game.player["inventory"].append("hermits_strategy")
        
        return True
    
    def event_meet_wandering_knight(self, parameters=None):
        """Meeting Sir Galwynne at the crossroads"""
        self.display_story_text([
            "At the crossroads stands a weathered knight whose armor bears neither the insignia of White nor Black.",
            "Instead, a gray chess knight decorates his tunic. He observes you with keen eyes as you approach.",
            "\"Hail, traveler,\" he greets you. \"I am Sir Galwynne, once of the White Kingdom, now serving only the balance.\"",
            "He gestures to the paths stretching in different directions.",
            "\"You stand at a crossroads both literal and figurative. East leads toward the Black Kingdom, north to the White Highlands, and beyond to both realms' capitals.\"",
            "Sir Galwynne studies you thoughtfully.",
            "\"These kingdoms have remained in stalemate for generations. Some believe this balance is sacred; others that it must eventually break.\"",
            "He produces a travel chess set from his pack.",
            "\"Before you choose your path, perhaps a game? I find chess reveals much about a person's nature.\""
        ])
        
        self.story_flags["met_wandering_knight"] = True
        return True
    
    def event_alignment_choice(self, parameters=None):
        """Offering the player a choice of alignment"""
        alignment = parameters.get("choice", None) if parameters else None
        
        if alignment == "white":
            self.display_story_text([
                "\"I see in you the values of the White Kingdom,\" Sir Galwynne observes. \"Order, honor, tradition.\"",
                "\"The path north leads to the White Highlands. There you'll find Castle Lumina welcoming those who uphold its ideals.\"",
                "He presents you with a white pawn carved from ivory.",
                "\"A token that may open doors among those loyal to Albion. Use it wisely.\""
            ])
            self.game.player["alignment"] = "white"
            self.story_flags["aligned_white"] = True
            
            # Add item to inventory
            if "white_kingdom_token" not in self.game.player["inventory"]:
                self.game.player["inventory"].append("white_kingdom_token")
        
        elif alignment == "black":
            self.display_story_text([
                "\"I see in you the values of the Black Kingdom,\" Sir Galwynne observes. \"Ambition, adaptability, pragmatism.\"",
                "\"The path east leads toward Noir. Those with your talents might find opportunity in its meritocratic society.\"",
                "He presents you with a black pawn carved from obsidian.",
                "\"A token that may open doors among those loyal to Noir. Use it wisely.\""
            ])
            self.game.player["alignment"] = "black"
            self.story_flags["aligned_black"] = True
            
            # Add item to inventory
            if "black_kingdom_token" not in self.game.player["inventory"]:
                self.game.player["inventory"].append("black_kingdom_token")
        
        elif alignment == "neutral":
            self.display_story_text([
                "\"I see in you a balanced perspective,\" Sir Galwynne says with approval. \"Neither White nor Black, but something in between.\"",
                "\"Those who walk the middle path face challenges from both sides, but also see opportunities invisible to others.\"",
                "He presents you with a gray pawn carved from strange, shimmer ing stone.",
                "\"A token of neutrality. Few recognize its significance, but those who do will know you as a potential arbiter.\""
            ])
            self.game.player["alignment"] = "neutral"
            self.story_flags["aligned_neutral"] = True
            
            # Add item to inventory
            if "neutral_arbiter_token" not in self.game.player["inventory"]:
                self.game.player["inventory"].append("neutral_arbiter_token")
        
        return True
    
    def event_discover_prophecy(self, parameters=None):
        """Discovering the Prophecy of the Final Checkmate"""
        self.display_story_text([
            "The ancient scroll crackles as you carefully break the seal and unroll it.",
            "Written in faded ink, you find what appears to be a prophecy:",
            "",
            "\"When a player of neither white nor black achieves the ultimate checkmate,",
            "the eternal stalemate shall end and the realms reunite.\"",
            "",
            "Below the text is a diagram of a chess position unlike any you've seen,",
            "with pieces arranged in a pattern that seems to violate the rules of the game.",
            "Yet somehow, studying it gives you a strange sense of recognition,",
            "as if the pattern connects to something profound about the world itself."
        ])
        
        self.story_flags["discovered_prophecy"] = True
        return True
    
    def event_chapter_transition(self, parameters=None):
        """Transition to a new chapter"""
        new_chapter = parameters.get("chapter", None) if parameters else None
        
        if new_chapter and new_chapter in self.chapters:
            chapter_name = self.chapters[new_chapter]
            
            self.display_story_text([
                "=" * 60,
                f"CHAPTER {new_chapter[-1]}: {chapter_name.upper()}",
                "=" * 60,
                "",
                f"You have completed the previous chapter and now begin {chapter_name}.",
                "New challenges and opportunities await as your journey continues.",
                "The choices you've made so far will influence the path ahead.",
                "",
                "=" * 60
            ])
            
            self.current_chapter = new_chapter
            return True
        
        return False
    
    def event_random_encounter(self, parameters=None):
        """Random encounter event"""
        encounter_type = parameters.get("type", None) if parameters else None
        
        # This is a placeholder - actual implementation would depend on the encounter system
        if encounter_type:
            # Process the encounter based on type
            return True
        
        return False
    
    def event_chess_tip(self, parameters=None):
        """Provide a random chess tip"""
        tips = [
            "Control the center of the board early to maximize your options.",
            "Knights are powerful in closed positions, while bishops excel in open ones.",
            "Castle early to protect your king and connect your rooks.",
            "Think of pawns not as expendable, but as future queens waiting to promote.",
            "When ahead in material, look to exchange pieces but not pawns.",
            "Before moving, ask yourself: What is my opponent threatening?",
            "The player who controls more space often has more strategic options.",
            "A knight on the rim is dim; a knight in the center is better.",
            "In endgames, activate your king - it becomes a powerful attacking piece.",
            "Don't move the same piece twice in the opening unless necessary."
        ]
        
        tip = random.choice(tips)
        
        self.display_story_text([
            "CHESS TIP:",
            f"{tip}"
        ])
        
        return True
    
    def display_story_text(self, text_lines):
        """Display story text with appropriate formatting"""
        # In a full implementation, this would be integrated with the game's
        # text display system. For now, it's a simple placeholder.
        import os
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        for line in text_lines:
            print(line)
        print("\n" + "=" * 60)
        input("\nPress Enter to continue...")
    
    def get_current_objective(self):
        """Get the current main objective based on story flags"""
        # Simple decision tree to determine current objective
        if not self.story_flags["met_elder_thomas"]:
            return "Explore the White Village and meet with Elder Thomas"
        
        if not self.story_flags["defeated_rowan"]:
            return "Challenge and defeat Rowan the Black Bandit in the town square"
        
        if not self.story_flags["met_hermit"]:
            return "Seek out the Hermit in the forest clearing for advanced chess training"
        
        if not self.story_flags["completed_hermit_training"]:
            return "Complete Elowen the Hermit's chess training"
        
        if not self.story_flags["met_wandering_knight"]:
            return "Travel to the Crossroads and meet Sir Galwynne"
        
        if not (self.story_flags["aligned_white"] or self.story_flags["aligned_black"] or self.story_flags["aligned_neutral"]):
            return "Choose your alignment with Sir Galwynne's guidance"
        
        # Default if all early objectives are complete
        return "Continue your journey into the wider Chess Realms"
    
    def get_side_objectives(self):
        """Get a list of available side objectives"""
        objectives = []
        
        if self.story_flags["met_elder_thomas"] and not self.story_flags["discovered_prophecy"]:
            objectives.append("Find and translate the mysterious scroll in the forest")
        
        # Add more side objectives as needed
        
        return objectives
