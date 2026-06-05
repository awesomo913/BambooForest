# From: audio.py:217
# Toggle sound on/off.

    def toggle(self) -> None:
        """Toggle sound on/off."""
        self.enabled = not self.enabled
