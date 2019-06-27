"""fdtool.__main__: executed when fdtool directory is called as script."""
import multiprocessing, time, sys
from .fdtool import main
from .config import MAX_TIME


# Start main as a process
p = multiprocessing.Process(target=main, name="Main")
p.start()
# Wait for main
p.join(MAX_TIME)

# If thread is active
if p.is_alive():
    # Print exceeded time limit
    print("\n", "Exceeded preset time limit."); sys.stdout.flush()
    # Terminate main
    p.terminate()
    # Cleanup
    p.join()
