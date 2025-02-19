import uuid as u
import hashlib as h
from datetime import datetime as d

def a():
    return str(u.uuid1())

def b():
    t = d.now()
    w = t.isocalendar()[1]
    return str(w)

def c():
    x = a()[-6:-2]
    y = b()
    z = "H917724495"
    f = x + y + z
    g = h.sha256(f.encode()).hexdigest()
    return g[-6:]