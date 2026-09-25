"""A few dozen realistic, messy order emails to run extraction on.

Deliberately inconsistent formatting, abbreviations, and typos, since that's
the whole point of the exercise — this is what Unilog's HyperScale has to
handle in production.
"""

SAMPLE_EMAILS = [
    """Hi, need the following for the Elm St job ASAP:
    - 10x 1/2" copper elbow
    - 4 ea 3/4 in PVC coupling
    - two circuit breakers
    Please rush, crew is on site tomorrow.""",
    """order for warehouse restock:
    qty 25 - 1 inch brass valve
    qty 6 - thermostat (any brand fine)
    qty 100 - wire nuts
    """,
    """Morning — can you send:
    3 blower motors
    a couple duct elbows, 2in
    1 refrigerant line
    no rush on this one""",
    """PO#4471 items needed:
    - Union, steel, 3/4"
    - 12x outlet
    - 5 conduit (electrical)
    Deliver by Friday please.""",
    """hey can u get me 8 pex couplings 1/2 inch and also 2 filters for the hvac unit,
    thx""",
    """Order:
    1) 15 x galvanized reducer 1.5"
    2) 20 x switch (standard)
    3) 4 x vent grille
    Urgent - customer waiting""",
    """need copper tee x6 (3/4") and 2 junction boxes, when you get a chance""",
    """Restocking electrical aisle:
    - 30 circuit breakers
    - 15 outlets
    - 50 wire nuts
    - 10 conduit sections""",
    """for the Miller residence job:
    2 PVC caps 1"
    1 blower motor
    3 thermostats
    please confirm availability""",
    """quick order — 6x brass adapter half inch, and one refrigerant line, thanks""",
]
