"""fdtool.__main__: executed when fdtool directory is called as script."""
import multiprocessing, time, sys
from fdtool import main

# Start main as a process
p = multiprocessing.Process(target=main, name="Main")
p.start()
# Wait 4 hours for main
p.join(14400)

# If thread is active
if p.is_alive():
    # Print exceeded time limit
    print "\n", "Exceeded preset time limit of 4 hours."; sys.stdout.flush()
    # Terminate main
    p.terminate()
    # Cleanup
    p.join()
