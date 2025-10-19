"""
History management for TTS generations.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class HistoryManager:
    """Manages generation history using JSON storage."""

    def __init__(self, history_file: Path):
        """
        Initialize history manager.

        Args:
            history_file: Path to JSON file for storing history
        """
        self.history_file = Path(history_file)
        self._ensure_history_file()

    def _ensure_history_file(self):
        """Create history file if it doesn't exist."""
        if not self.history_file.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_history([])

    def _load_history(self) -> List[Dict]:
        """
        Load history from JSON file.

        Returns:
            List of generation records
        """
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            return []

    def _save_history(self, history: List[Dict]):
        """
        Save history to JSON file.

        Args:
            history: List of generation records
        """
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_generation(
        self,
        voice_name: str,
        text_source: str,
        text_length: int,
        wav_path: str,
        mp3_path: Optional[str] = None,
        chunk_count: int = 0,
        parameters: Optional[Dict] = None
    ) -> bool:
        """
        Add a new generation to history.

        Args:
            voice_name: Name of voice used
            text_source: Name or description of text source
            text_length: Length of text in characters
            wav_path: Path to generated WAV file
            mp3_path: Path to generated MP3 file (optional)
            chunk_count: Number of chunks (0 for single-pass)
            parameters: Dictionary of TTS parameters used

        Returns:
            True if successful
        """
        history = self._load_history()

        record = {
            'id': len(history) + 1,
            'timestamp': datetime.now().isoformat(),
            'voice_name': voice_name,
            'text_source': text_source,
            'text_length': text_length,
            'wav_path': wav_path,
            'mp3_path': mp3_path,
            'chunk_count': chunk_count,
            'mode': 'chunked' if chunk_count > 0 else 'single-pass',
            'parameters': parameters or {}
        }

        history.append(record)
        self._save_history(history)
        return True

    def get_all_generations(self) -> List[Dict]:
        """
        Get all generation records.

        Returns:
            List of generation records, sorted by timestamp (newest first)
        """
        history = self._load_history()
        return sorted(history, key=lambda x: x.get('timestamp', ''), reverse=True)

    def get_generations_by_voice(self, voice_name: str) -> List[Dict]:
        """
        Get all generations for a specific voice.

        Args:
            voice_name: Name of the voice

        Returns:
            List of generation records for that voice
        """
        history = self._load_history()
        filtered = [h for h in history if h.get('voice_name') == voice_name]
        return sorted(filtered, key=lambda x: x.get('timestamp', ''), reverse=True)

    def get_generation_by_id(self, generation_id: int) -> Optional[Dict]:
        """
        Get a specific generation by ID.

        Args:
            generation_id: ID of the generation

        Returns:
            Generation record or None if not found
        """
        history = self._load_history()
        for record in history:
            if record.get('id') == generation_id:
                return record
        return None

    def delete_generation(self, generation_id: int) -> bool:
        """
        Delete a generation from history.

        Args:
            generation_id: ID of the generation to delete

        Returns:
            True if successful
        """
        history = self._load_history()
        original_length = len(history)
        history = [h for h in history if h.get('id') != generation_id]

        if len(history) < original_length:
            self._save_history(history)
            return True
        return False

    def clear_history(self) -> bool:
        """
        Clear all history.

        Returns:
            True if successful
        """
        self._save_history([])
        return True

    def get_statistics(self) -> Dict:
        """
        Get statistics about generations.

        Returns:
            Dictionary with statistics
        """
        history = self._load_history()

        if not history:
            return {
                'total_generations': 0,
                'unique_voices': 0,
                'total_characters': 0,
                'chunked_generations': 0,
                'single_pass_generations': 0
            }

        voices = set(h.get('voice_name') for h in history)
        total_chars = sum(h.get('text_length', 0) for h in history)
        chunked = sum(1 for h in history if h.get('chunk_count', 0) > 0)
        single = len(history) - chunked

        return {
            'total_generations': len(history),
            'unique_voices': len(voices),
            'total_characters': total_chars,
            'chunked_generations': chunked,
            'single_pass_generations': single,
            'voices_used': sorted(list(voices))
        }

    def export_to_csv(self, output_path: Path) -> bool:
        """
        Export history to CSV file.

        Args:
            output_path: Path for CSV export

        Returns:
            True if successful
        """
        import csv

        history = self._load_history()

        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if not history:
                    return True

                fieldnames = ['id', 'timestamp', 'voice_name', 'text_source',
                              'text_length', 'mode', 'chunk_count', 'wav_path', 'mp3_path']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
                for record in history:
                    row = {k: record.get(k, '') for k in fieldnames}
                    writer.writerow(row)

            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
