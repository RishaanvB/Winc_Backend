# Do not modify these lines
__winc_id__ = "7b9401ad7f544be2a23321292dd61cb6"
__human_name__ = "arguments"

# Add your code after this line


# part 1 Greet Template


""" A greeting template (str). Set this template parameter to 'Hello, <name>!' by default."""
# Zie bovenstaande regel, ik weet niet hoe je een variable = x
# als  2e parameter kan doorgeven, waarbij def f(a, b="string" + a)


def greet(name, greet_template="Hello"):
    """wincpy geeft hier een error voor  "greet handles an optional template
    string correctly", weet niet precies wat hier nu verwacht wordt
    als 2e param"""
    return f"{greet_template}, {name}!"


# part 2 Force


def force(mass: float, body="earth"):
    # wss niet nauwkeurig met grote mass door het gebruik van rounded()
    celestial_bodies = {
        "Sun": 274,
        "Jupiter": 24.92,
        "Neptune": 11.15,
        "Saturn": 10.44,
        "Earth": 9.798,
        "Uranus": 8.87,
        "Venus": 8.87,
        "Mars": 3.71,
        "Mercury": 3.7,
        "Moon": 1.62,
        "Pluto": 0.58,
    }
    mass = float(mass)
    surface_gravity = celestial_bodies[body.lower().capitalize()]
    surface_gravity_rounded = round(float(surface_gravity), 1)
    gravity = surface_gravity_rounded
    force_newton = mass * gravity
    return force_newton


# Part 3 Gravity


def pull(m1: "float in kg", m2: "float in kg", d: "distance"):

    g = 6.674 * 10 ** -11
    gravitational_pull = g * ((m1 * m2) / (d ** 2))
    return gravitational_pull
