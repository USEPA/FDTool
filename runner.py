"""Convenience wrapper for running fdtool directly from source tree."""
import multiprocessing, time, sys
from fdtool.fdtool import main

if __name__ == '__main__':
    
    # Start main as a process
    p = multiprocessing.Process(target=main, name="Main")
    p.start()
    # Wait 4 hours for main
    p.join(1440)
    
    # If thread is active
    if p.is_alive():
        # Print exceeded time limit
        print "\n","Exceeded preset time limit of 4 hours."; sys.stdout.flush()
        # Terminate main
        p.terminate()
        # Cleanup
        p.join()

