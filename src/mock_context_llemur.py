"""
Mock context-llemur for testing our CLI features
"""
from pathlib import Path

class CtxCore:
    """Mock CtxCore class to simulate context-llemur functionality"""
    
    def get_active_ctx_path(self):
        """Return current directory as the active context path"""
        return Path.cwd()