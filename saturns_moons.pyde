########### REFERENCES ###########
"""
https://en.wikipedia.org/wiki/Janus_(moon)
https://en.wikipedia.org/wiki/Epimetheus_(moon)
https://en.wikipedia.org/wiki/Gravitational_constant
https://py.processing.org/reference/

Coding Train: The Nature of Code 2
https://www.youtube.com/playlist?list=PLRqwX-V7Uu6ZV4yEcW3uDwOgGXKUUsPOM
"""

########### CLASS DEFINITION ###########
  
class Planet(object):
    """
    Based on: Coding Train: The Nature of Code 2
    https://www.youtube.com/playlist?list=PLRqwX-V7Uu6ZV4yEcW3uDwOgGXKUUsPOM

    """
    def __init__(self, m, x, y):
        self.mass = m
        self.position = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0,0)
        self.look = (200, 50, 50)  # RGB: default look for Saturn
        self.draw_size = 61  # default scale for Saturn: to scale should be 61 pixels 
        self.history = []  # history of path to draw trail
        self.max_history = 5
        self.trail_opacity = 20
        
    def applyForce(self, force):
        f = PVector.div(force, self.mass)
        self.acceleration.add(f)
    
    def update(self):
        self.velocity.add(self.acceleration)
        self.position.add(self.velocity)
        self.acceleration.mult(0)
        
        self.history.append(self.position.copy())  # update the path
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def display(self):    
        noStroke()
        fill(*self.look)
        ellipse(self.position.x, self.position.y, self.draw_size, self.draw_size)
        beginShape()
        
        # trail from history
        noFill()
        beginShape()
        stroke(self.look[0], self.look[1], self.look[2], self.trail_opacity)
        for pos in self.history:
            vertex(pos.x, pos.y)
            noFill()
            strokeWeight(self.draw_size)
        endShape()
        noStroke()

    def attract(self, m, G):
        force = PVector.sub(self.position, m.position)
        distance = force.mag()
        force.normalize()
        strength = (G * self.mass * m.mass) / (distance * distance)
        force.mult(strength)
        return force


########### INPUTS / SCENARIOS ###########

# CHOOSE THE SCENARIO:
scenarios = ['default', 'rotating', 'exaggerated']
scenario = scenarios[1] 

# inputs to draw() and setup based on scenario
if scenario == scenarios[0]:
    opacity = 220
    scale_factor = 3
    angle_increment = 0
    size_x, size_y = 1200, 1200
    fps = 24
elif scenario == scenarios[1]:
    opacity = 1
    scale_factor = 1
    angle_increment = 0.1035135 
    # from trial and error,
    # .1035135 is very close, maybe super-slightly too counterclockwise  
    # .103513 very very slightly too much counterclockwise
    # .103512 slightly too much counterclockwise
    # .103515 way too clockwise
    size_x, size_y = 400, 400
    fps = 6000
elif scenario == scenarios[2]:
    opacity = 60
    scale_factor = 0.5
    angle_increment = 0
    size_x, size_y = 1200, 1200
    fps = 240


########### SETUP ###########

def setup():

    size(size_x, size_y)
    frameRate(fps)
    
    global angle
    angle = 0

    global G
    global SATURN
    global JANUS
    global EPIMETHEUS
    
    # scaled constants
    G = 0.000006674300
    m_s = 5683400000  # removing 2 sig figs actually makes a big difference
    
    if scenario == scenarios[0] or scenario == scenarios[1]:
        # DEFAULT ORBITS
        m_j, o_j, v_j = 18.975, 152.035, 15.7955656926356
        m_e, o_e, v_e = 5.266, 152.085, -15.792968976299744
        orbital_correction = 8  # number of pixels of correction to orbit
    else:
        # EXAGGERATED ORBITS
        m_j, o_j, v_j = 1000000, 480, 8.9
        m_e, o_e, v_e = 100000, 450, -9.2
        orbital_correction = 4  # number of pixels of correction to orbit
    
    SATURN = Planet(m_s, 0, 0)
    SATURN.draw_size = 61  # actual scale: should be 61 pixels
    
    JANUS = Planet(m_j, orbital_correction, o_j)
    JANUS.velocity = PVector(v_j, 0)
    JANUS.look = (239, 65, 239)
    JANUS.draw_size = 9  # actual scale: should be 0.09 pixels
    
    EPIMETHEUS = Planet(m_e, -orbital_correction, -o_e)
    # EPIMETHEUS.velocity = PVector(v_e, 0)
    EPIMETHEUS.velocity.x = v_e
    EPIMETHEUS.look = (102, 202, 102)
    EPIMETHEUS.draw_size = 6  # actual scale: should be 0.06 pixels 
    
    if scenario == scenarios[2]: 
        SATURN.draw_size = 240
        JANUS.draw_size = 60
        EPIMETHEUS.draw_size = 40 
        
    if scenario in ['rotating', 'exaggerated']: 
        SATURN.trail_opacity = 0
        JANUS.trail_opacity = 0
        EPIMETHEUS.trail_opacity = 0 
    
    background(0)


########### DRAW ###########

def draw():
    
    fill(0, opacity)
    rect(0, 0, width, height)
    
    translate(width/2, height/2)
    
    scale(scale_factor)
    
    # rotating reference frame
    global angle
    rotate(angle)
    angle += angle_increment
    
    force = SATURN.attract(JANUS, G)
    JANUS.applyForce(force)
    force = EPIMETHEUS.attract(JANUS, G)
    JANUS.applyForce(force)
    
    force = SATURN.attract(EPIMETHEUS, G)
    EPIMETHEUS.applyForce(force)
    force = JANUS.attract(EPIMETHEUS, G)
    EPIMETHEUS.applyForce(force)
    
    JANUS.update()
    EPIMETHEUS.update()
    
    SATURN.display()
    JANUS.display()
    EPIMETHEUS.display()
    
    # debug dialogue for scenario[1]
    # print("approx number of orbits: " + str(angle / (2 * PI)))
    
    # debug framerate
    # println(frameRate)
    # println(frameCount)
