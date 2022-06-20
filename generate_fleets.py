import random

def generate_fleet(faction,fileout=''):
    military_names = ['Patrol','Navy','Guard','Security','Military','Defense']
    civilian_names = ['Merchant','Civilian','Privateer']
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} fleets.txt'
    fleetwrite = open(fileout, 'w')

    fleet_name = faction.name + ' ' + random.choice(military_names)
    names = faction.name + ' names'
    personalities = "heroic opportunistic"

    #fleet_tactic = random.choice('defense offense balance hitrun kite'.split())
    fleet_composition = {}
    if faction.fleet_tactic == 'defense':
        for ship in faction.shiplist:
            if ship.category == 'Heavy Warship':
                fleet_composition[ship.name] = random.randrange(1,5)
    fleetwrite.write(f'fleet "{fleet_name}"' + '\n')
    fleetwrite.write(f'\tgovernment "{faction.name}"' + '\n')
    fleetwrite.write(f'\tnames "{names}"' + '\n')
    fleetwrite.write(f'\tpersonality' + '\n')
    fleetwrite.write(f'\t\t{personalities}' + '\n')
    for n in range(random.randrange(1,6)):
        weight = round((n+1)*random.randrange(2,20))
        for i in range(len(faction.shiplist)):
            ship1 = random.choice(faction.shiplist)
            if ship1.installed_weapons > 0:
                break
        for i in range(len(faction.shiplist)):
            ship2 = random.choice(faction.shiplist)
            if ship2.installed_weapons > 0:
                break
        for i in range(len(faction.shiplist)):
            ship3 = random.choice(faction.shiplist)
            if ship3.installed_weapons > 0:
                break
        ship1_count = random.randrange(1,5)
        ship2_count = random.randrange(1,5)
        ship3_count = random.randrange(1,5)
        fleetwrite.write(f'\tvariant {weight}'+ '\n')
        fleetwrite.write(f'\t\t"{ship1.name}" {ship1_count}' + '\n')
        fleetwrite.write(f'\t\t"{ship2.name}" {ship2_count}' + '\n')
        fleetwrite.write(f'\t\t"{ship3.name}" {ship3_count}' + '\n')

    faction.patrolfleets.append(fleet_name)

    fleet_name = faction.name + ' ' + random.choice(civilian_names)
    personalities = "timid"

    fleetwrite.write(f'fleet "{fleet_name}"' + '\n')
    fleetwrite.write(f'\tgovernment "{faction.name}"' + '\n')
    fleetwrite.write(f'\tnames "{names}"' + '\n')
    fleetwrite.write(f'\tpersonality' + '\n')
    fleetwrite.write(f'\t\t{personalities}' + '\n')
    for n in range(random.randrange(1,6)):
        weight = round(n*random.randrange(2,20))
        ship1 = random.choice(faction.shiplist)
        ship2 = random.choice(faction.shiplist)
        ship3 = random.choice(faction.shiplist)
        ship1_count = random.randrange(1,5)
        ship2_count = random.randrange(1,5)
        ship3_count = random.randrange(1,5)
        fleetwrite.write(f'\tvariant {weight}'+ '\n')
        fleetwrite.write(f'\t\t"{ship1.name}" {ship1_count}' + '\n')
        fleetwrite.write(f'\t\t"{ship2.name}" {ship2_count}' + '\n')
        fleetwrite.write(f'\t\t"{ship3.name}" {ship3_count}' + '\n')

    faction.civilianfleets.append(fleet_name)

    fleetwrite.close()
