#%%
from numpy import abs, sin
from matplotlib import pyplot
from processor import Processor

p = Processor(('127.0.0.1', 5050), 2, 44100, 2)
chunk = [abs(2000 * sin(x * 8*3.1415/88200)) for x in range(88200)]

pyplot.figure()
pyplot.plot(chunk)

smooth = p.smooth(chunk)
pyplot.figure()
pyplot.plot(smooth)

window = p.window(smooth)
pyplot.figure()
pyplot.plot(window)

flanks = p.flanks(window)
pyplot.figure()
pyplot.plot(flanks, '.')

dominant = p.dominant(flanks)
pyplot.figure()
pyplot.plot(dominant, '.')

p.generate_osc(dominant)

# %%
