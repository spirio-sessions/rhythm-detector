#%%
from numpy import abs, sin
from matplotlib import pyplot
from analyser import Analyser

a = Analyser(44100, 2)
chunk = [abs(2000 * sin(x * 8*3.1415/88200)) for x in range(88200)]

pyplot.figure()
pyplot.plot(chunk)

smooth = a.smooth(chunk)
pyplot.figure()
pyplot.plot(smooth)

window = a.window(smooth)
pyplot.figure()
pyplot.plot(window)

flanks = a.flanks(window)
pyplot.figure()
pyplot.plot(flanks, '.')

dominant = a.dominant(flanks)
pyplot.figure()
pyplot.plot(dominant, '.')

# %%
