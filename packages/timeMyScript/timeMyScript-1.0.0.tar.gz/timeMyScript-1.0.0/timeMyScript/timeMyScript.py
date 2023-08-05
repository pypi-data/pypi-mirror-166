import atexit
def exit_handler(start):
	end = time.time()
	total_time = end - start
	print(f'Timer provided by timeMyScript: {str(total_time)} s')

import time

start = time.time()
atexit.register(exit_handler, start)



