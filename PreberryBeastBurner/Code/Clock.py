from time import perf_counter_ns, sleep

class Clock:
	def __init__(s, fps=60):
		s.start = perf_counter_ns()
		s.delta = (10**9)/fps

		s.ticks = 0
		s.timeSkips = 0
		s.timeSkipped = 0

	def tick(s):
		stop = s.start + s.delta
		cur = perf_counter_ns()
		if cur < stop:
			sleep((stop-cur)/(10**9))
			s.start = stop
		else:
			s.start = cur
			s.timeSkips += 1
			s.timeSkipped += s.start - stop

		s.ticks += 1

	def setFps(s, fps):
		s.delta = (10 ** 9)/fps