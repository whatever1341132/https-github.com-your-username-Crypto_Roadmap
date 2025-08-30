"""Mnemonic functionality for crypto roadmap."""

import hashlib
import secrets


class MnemonicGenerator:
    """Simple mnemonic generator for demonstration purposes."""
    
    # Basic word list for demonstration
    WORD_LIST = [
        "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
        "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
        "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
        "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
        "advice", "aerobic", "affair", "afford", "afraid", "again", "agent", "agree",
        "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol",
        "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha",
        "already", "also", "alter", "always", "amateur", "amazing", "among", "amount",
        "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry", "animal",
        "ankle", "announce", "annual", "another", "answer", "antenna", "antique", "anxiety",
        "any", "apart", "apology", "appear", "apple", "approve", "april", "arcade",
        "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor",
        "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
        "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume",
        "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
        "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado",
        "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis"
    ]
    
    def __init__(self):
        """Initialize the mnemonic generator."""
        pass
    
    def generate_mnemonic(self, word_count=12):
        """Generate a mnemonic phrase with specified word count."""
        if word_count not in [12, 15, 18, 21, 24]:
            raise ValueError("Word count must be 12, 15, 18, 21, or 24")
        
        # Generate random entropy
        entropy_bits = (word_count * 11) - (word_count // 3)
        entropy = secrets.randbits(entropy_bits)
        
        # Convert to words (simplified implementation)
        words = []
        for _ in range(word_count):
            word_index = entropy % len(self.WORD_LIST)
            words.append(self.WORD_LIST[word_index])
            entropy = entropy >> 11
        
        return " ".join(words)
    
    def validate_mnemonic(self, mnemonic):
        """Basic validation of mnemonic phrase."""
        if not mnemonic or not isinstance(mnemonic, str):
            return False
        
        words = mnemonic.strip().split()
        
        # Check word count
        if len(words) not in [12, 15, 18, 21, 24]:
            return False
        
        # Check if all words are in the word list
        for word in words:
            if word.lower() not in [w.lower() for w in self.WORD_LIST]:
                return False
        
        return True
    
    def mnemonic_to_seed(self, mnemonic, passphrase=""):
        """Convert mnemonic to seed (simplified implementation)."""
        if not self.validate_mnemonic(mnemonic):
            raise ValueError("Invalid mnemonic")
        
        # Simple seed generation using PBKDF2
        salt = f"mnemonic{passphrase}".encode('utf-8')
        seed = hashlib.pbkdf2_hmac('sha512', mnemonic.encode('utf-8'), salt, 2048)
        return seed.hex()