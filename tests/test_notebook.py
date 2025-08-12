import pytest
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from memory.notebook import NotebookManager

@pytest.fixture
def temp_ctx():
    """Create temporary context directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_notebook_add(temp_ctx):
    manager = NotebookManager(temp_ctx)
    success, message = manager.add("test_key", "test_value")
    assert success
    assert "Stored" in message

def test_notebook_limits(temp_ctx):
    manager = NotebookManager(temp_ctx)
    
    # Test max entries
    for i in range(30):
        manager.add(f"key{i}", "value")
    
    success, message = manager.add("key31", "value")
    assert not success
    assert "full" in message

def test_notebook_get(temp_ctx):
    manager = NotebookManager(temp_ctx)
    manager.add("test", "value123")
    
    entry = manager.get("test")
    assert entry is not None
    assert entry['value'] == "value123"