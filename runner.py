"""Convenience wrapper for running fdtool directly from source tree."""
import multiprocessing, time, sys
from fdtool.fdtool import main
from fdtool.config import MAX_TIME

if __name__ == '__main__':
    
    # Start main as a process
    p = multiprocessing.Process(target=main, name="Main")
    p.start()
    # Wait for main
    p.join(MAX_TIME)
    
    # If thread is active
    if p.is_alive():
        # Print exceeded time limit
        print "\n","Exceeded preset time limit."; sys.stdout.flush()
        # Terminate main
        p.terminate()
        # Cleanup
        p.join()

