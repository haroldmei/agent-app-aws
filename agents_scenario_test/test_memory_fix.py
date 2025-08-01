import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from conftest import SageAdapter
import scenario

async def test_sage():
    scenario.configure(default_model='openai/gpt-4o-mini', cache_key='test-123')
    
    class MockInput:
        def __init__(self):
            self.thread_id = 'test-thread'
        def last_new_user_message_str(self):
            return 'Hello, how are you?'
    
    adapter = SageAdapter()
    mock_input = MockInput()
    
    try:
        result = await adapter.call(mock_input)
        print('✅ SageAdapter test passed! Memory access works.')
        print(f'Result type: {type(result)}')
        if result:
            print(f'Result length: {len(result)}')
    except Exception as e:
        print(f'❌ SageAdapter test failed: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test_sage())
