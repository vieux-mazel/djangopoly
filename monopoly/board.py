"""Describes the board of Monopoly."""

streets = [
    {
        'type': 'street',
        'color': '#955335'
    },
    {
        'type': 'street',
        'color': '#AAE0FA'
    },
    {
        'type': 'street',
        'color': '#D93A96'
    },
    {
        'type': 'street',
        'color': '#F7941D'
    },
    {
        'type': 'street',
        'color': '#ED1B24'
    },
    {
        'type': 'street',
        'color': '#FEF200'
    },
    {
        'type': 'street',
        'color': '#1FB25A'
    },
    {
        'type': 'street',
        'color': '#0072BB'
    },
]

properties = [
    {
        'type': 'property',
        'position': 1,
        'title': 'Old Kent Toad',
        'street': '#955335',
        'tax_site': 2,
        'price': 60,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 3,
        'title': 'Whitechapel Road',
        'street': '#955335',
        'tax_site': 4,
        'price': 60,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 6,
        'title': 'The Angel Inslington',
        'street': '#AAE0FA',
        'tax_site': 6,
        'price': 100,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 8,
        'title': 'Euston Road',
        'street': '#AAE0FA',
        'tax_site': 6,
        'price': 100,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 9,
        'title': 'Penton View Road',
        'street': '#AAE0FA',
        'tax_site': 8,
        'price': 100,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 11,
        'title': 'Pall Mall',
        'street': '#D93A96',
        'tax_site': 10,
        'price': 140,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 13,
        'title': 'White Hall',
        'street': '#D93A96',
        'tax_site': 10,
        'price': 140,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 14,
        'title': 'Norton Avenue',
        'street': '#D93A96',
        'tax_site': 10,
        'price': 160,
        'house_price': 100,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 16,
        'title': 'Bow Street',
        'street': '#F7941D',
        'tax_site': 14,
        'price': 180,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 18,
        'title': 'Marlboro Street',
        'street': '#F7941D',
        'tax_site': 14,
        'price': 180,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 19,
        'title': 'Vine Street',
        'street': '#F7941D',
        'tax_site': 16,
        'price': 200,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 21,
        'title': 'Strand',
        'street': '#ED1B24',
        'tax_site': 16,
        'price': 220,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 23,
        'title': 'Fleet Street',
        'street': '#ED1B24',
        'tax_site': 18,
        'price': 220,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 24,
        'title': 'Trafalgar Square',
        'street': '#ED1B24',
        'tax_site': 20,
        'price': 240,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 26,
        'title': 'Lester Square',
        'street': '#FEF200',
        'tax_site': 22,
        'price': 260,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 27,
        'title': 'Coventry Street',
        'street': '#FEF200',
        'tax_site': 22,
        'price': 260,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 29,
        'title': 'Picadilly',
        'street': '#FEF200',
        'tax_site': 24,
        'price': 280,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 31,
        'title': 'Regent Street',
        'street': '#1FB25A',
        'tax_site': 24,
        'price': 300,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 32,
        'title': 'Oxford Street',
        'street': '#1FB25A',
        'tax_site': 26,
        'price': 300,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 34,
        'title': 'Bond Street',
        'street': '#1FB25A',
        'tax_site': 28,
        'price': 320,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 37,
        'title': 'Park Lane',
        'street': '#0072BB',
        'tax_site': 35,
        'price': 350,
        'house_price': 100
    },
    {
        'type': 'property',
        'position': 39,
        'title': 'Mayfair',
        'street': '#0072BB',
        'tax_site': 50,
        'price': 400,
        'house_price': 100
    }
]

utilities = [
    {
        'type': 'utility',
        'position': 5,
        'title': 'Kings Cross Station',
        'price': 200,
        'tax_site': 25
    },
    {
        'type': 'utility',
        'position': 12,
        'title': 'Electric Company',
        'price': 150,
        'tax_site': 25
    },
    {
        'type': 'utility',
        'position': 15,
        'title': 'Maryleboan Station',
        'price': 200,
        'tax_site': 25
    },
    {
        'type': 'utility',
        'position': 25,
        'title': 'Fenchurchstreet Station',
        'price': 150,
        'tax_site': 25
    },
    {
        'type': 'utility',
        'position': 28,
        'title': 'Waterworks',
        'price': 150,
        'tax_site': 25
    },
    {
        'type': 'utility',
        'position': 35,
        'title': 'Liverpoolstreet Station',
        'price': 200,
        'tax_site': 25
    }
]

specials = [
    {
        'type': 'special',
        'position': 0,
        'title': 'Go',
        'effect':
            {
                'type': 'give_money',
                'param': 200
            }
    },
    {
        'type': 'special',
        'position': 2,
        'title': 'Community Chest',
        'effect':
            {
                'type': 'community_chest',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 4,
        'title': 'Income Tax',
        'effect':
            {
                'type': 'income_tax',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 7,
        'title': 'Chance',
        'effect':
            {
                'type': 'chance',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 10,
        'title': 'Jail',
        'effect':
            {
                'type': 'jail',
                'param': None,
            }
    },
    {
        'type': 'special',
        'position': 17,
        'title': 'Community Chest',
        'effect':
            {
                'type': 'community_chest',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 20,
        'title': 'Free Parking',
        'effect':
            {
                'type': 'free_parking',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 22,
        'title': 'Chance',
        'effect':
            {
                'type': 'chance',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 30,
        'title': 'Go to Jail',
        'effect':
            {
                'type': 'go_to_jail',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 33,
        'title': 'Community Chest',
        'effect':
            {
                'type': 'community_chest',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 36,
        'title': 'Chance',
        'effect':
            {
                'type': 'chance',
                'param': None
            }
    },
    {
        'type': 'special',
        'position': 38,
        'title': 'Supertax',
        'effect':
            {
                'type': 'supertax',
                'param': None
            }
    }
]

cards = [
    {
        'name': 'Advance to Go',
        'description': 'Mr. M strides in 7-league boots.',
        'effect':
            {
                'type': 'move',
                'param': 0
            }
    },
    {
        'name': 'Advance to The Angel Inslington',
        'description': 'Mr. M has tied a cloth bundle onto his cane to make a bindle, carried over his right shoulder, and is smoking a cigar.',
        'effect':
            {
                'type': 'move',
                'param': 6
            }
    },
    {
        'name': 'Bank pays you dividend of $50',
        'description': 'With his feet up on a telephone-bearing desk, Mr. M leans back in an overstuffed chair, blowing cigar smoke rings.',
        'effect':
            {
                'type': 'give_money',
                'param': 50,
            }
    },
    {
        'name': 'Go to Jail!',
        'description': 'A truncheon-carrying policeman in a dark-colored uniform hauls a surprised Mr M along by the feet.',
        'effect':
            {
                'type': 'go_to_jail',
                'param': 0,
            }
    },
    {
        'name': 'Pay poor tax of $15',
        'description': 'His trouser pockets pulled out to show them empty, Mr. M spreads his hands.',
        'effect':
            {
                'type': 'take_money',
                'param': 15
            }
    }
]

squares = sorted(properties + utilities + specials, key=lambda s: s['position'])
