
import sys
try:
    import moviepy.editor
    print("MoviePy imported successfully!")
except Exception as e:
    print(f"Error importing moviepy: {e}")
    import traceback
    traceback.print_exc()
