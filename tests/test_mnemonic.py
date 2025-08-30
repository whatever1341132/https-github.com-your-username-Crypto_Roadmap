#!/usr/bin/env python3
"""Tests for mnemonic functionality."""

import sys
import os
import unittest

# Add the parent directory to the path so we can import our package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_roadmap.mnemonic import MnemonicGenerator


class TestMnemonic(unittest.TestCase):
    """Test cases for MnemonicGenerator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = MnemonicGenerator()
    
    def test_mnemonic_generator_creation(self):
        """Test that we can create a MnemonicGenerator instance."""
        self.assertIsInstance(self.generator, MnemonicGenerator)
    
    def test_generate_mnemonic_default(self):
        """Test generating a default 12-word mnemonic."""
        mnemonic = self.generator.generate_mnemonic()
        words = mnemonic.split()
        self.assertEqual(len(words), 12)
        
        # Check that all words are from the word list
        for word in words:
            self.assertIn(word, self.generator.WORD_LIST)
    
    def test_generate_mnemonic_different_lengths(self):
        """Test generating mnemonics of different lengths."""
        for word_count in [12, 15, 18, 21, 24]:
            mnemonic = self.generator.generate_mnemonic(word_count)
            words = mnemonic.split()
            self.assertEqual(len(words), word_count)
    
    def test_generate_mnemonic_invalid_length(self):
        """Test that invalid word counts raise ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_mnemonic(10)
        
        with self.assertRaises(ValueError):
            self.generator.generate_mnemonic(25)
    
    def test_validate_mnemonic_valid(self):
        """Test validation of valid mnemonics."""
        # Generate a mnemonic and validate it
        mnemonic = self.generator.generate_mnemonic(12)
        self.assertTrue(self.generator.validate_mnemonic(mnemonic))
        
        # Test a known valid mnemonic
        valid_mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        self.assertTrue(self.generator.validate_mnemonic(valid_mnemonic))
    
    def test_validate_mnemonic_invalid(self):
        """Test validation of invalid mnemonics."""
        # Empty string
        self.assertFalse(self.generator.validate_mnemonic(""))
        
        # None
        self.assertFalse(self.generator.validate_mnemonic(None))
        
        # Wrong number of words
        self.assertFalse(self.generator.validate_mnemonic("abandon ability"))
        
        # Invalid words
        self.assertFalse(self.generator.validate_mnemonic("invalid words that are not in the wordlist"))
    
    def test_mnemonic_to_seed_valid(self):
        """Test converting valid mnemonic to seed."""
        mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        seed = self.generator.mnemonic_to_seed(mnemonic)
        
        # Check that we get a hex string
        self.assertIsInstance(seed, str)
        self.assertEqual(len(seed), 128)  # 64 bytes = 128 hex characters
        
        # Check that the same mnemonic produces the same seed
        seed2 = self.generator.mnemonic_to_seed(mnemonic)
        self.assertEqual(seed, seed2)
    
    def test_mnemonic_to_seed_with_passphrase(self):
        """Test converting mnemonic to seed with passphrase."""
        mnemonic = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        seed1 = self.generator.mnemonic_to_seed(mnemonic)
        seed2 = self.generator.mnemonic_to_seed(mnemonic, "passphrase")
        
        # Seeds should be different with and without passphrase
        self.assertNotEqual(seed1, seed2)
    
    def test_mnemonic_to_seed_invalid(self):
        """Test that invalid mnemonics raise ValueError when converting to seed."""
        with self.assertRaises(ValueError):
            self.generator.mnemonic_to_seed("invalid mnemonic")


if __name__ == "__main__":
    unittest.main()