"""Describes the board of Monopoly."""

streets = [
    {
        'type': 'street',
        'color': 'brown'
    },
    {
        'type': 'street',
        'color': 'light_blue'
    },
    {
        'type': 'street',
        'color': 'purple'
    },
    {
        'type': 'street',
        'color': 'orange'
    },
    {
        'type': 'street',
        'color': 'red'
    },
    {
        'type': 'street',
        'color': 'yellow'
    },
    {
        'type': 'street',
        'color': 'green'
    },
    {
        'type': 'street',
        'color': 'blue'
    },
]

properties = [
    {
        'type': 'property',
        'position': 1,
        'title': 'Old Kent Toad',
        'street': 'brown',
        'tax_site': 2,
        'price': 60
    },
    {
        'type': 'property',
        'position': 3,
        'title': 'Whitechapel Road',
        'street': 'brown',
        'tax_site': 4,
        'price': 60
    },
    {
        'type': 'property',
        'position': 6,
        'title': 'The Angel Inslington',
        'street': 'light_blue',
        'tax_site': 6,
        'price': 100
    },
    {
        'type': 'property',
        'position': 8,
        'title': 'Euston Road',
        'street': 'light_blue',
        'tax_site': 6,
        'price': 100
    },
    {
        'type': 'property',
        'position': 9,
        'title': 'Penton View Road',
        'street': 'light_blue',
        'tax_site': 8,
        'price': 100
    },
    {
        'type': 'property',
        'position': 11,
        'title': 'Pall Mall',
        'street': 'purple',
        'tax_site': 10,
        'price': 140
    },
    {
        'type': 'property',
        'position': 13,
        'title': 'White Hall',
        'street': 'purple',
        'tax_site': 10,
        'price': 140
    },
    {
        'type': 'property',
        'position': 14,
        'title': 'Norton Avenue',
        'street': 'purple',
        'tax_site': 10,
        'price': 160
    },
    {
        'type': 'property',
        'position': 16,
        'title': 'Bow Street',
        'street': 'orange',
        'tax_site': 14,
        'price': 180
    },
    {
        'type': 'property',
        'position': 18,
        'title': 'Marlboro Street',
        'street': 'orange',
        'tax_site': 14,
        'price': 180
    },
    {
        'type': 'property',
        'position': 19,
        'title': 'Vine Street',
        'street': 'orange',
        'tax_site': 16,
        'price': 200
    },
    {
        'type': 'property',
        'position': 21,
        'title': 'Strand',
        'street': 'red',
        'tax_site': 16,
        'price': 220
    },
    {
        'type': 'property',
        'position': 23,
        'title': 'Fleet Street',
        'street': 'red',
        'tax_site': 18,
        'price': 220
    },
    {
        'type': 'property',
        'position': 24,
        'title': 'Trafalgar Square',
        'street': 'red',
        'tax_site': 20,
        'price': 240
    },
    {
        'type': 'property',
        'position': 26,
        'title': 'Lester Square',
        'street': 'yellow',
        'tax_site': 22,
        'price': 260
    },
    {
        'type': 'property',
        'position': 27,
        'title': 'Coventry Street',
        'street': 'yellow',
        'tax_site': 22,
        'price': 260
    },
    {
        'type': 'property',
        'position': 29,
        'title': 'Picadilly',
        'street': 'yellow',
        'tax_site': 24,
        'price': 280
    },
    {
        'type': 'property',
        'position': 31,
        'title': 'Regent Street',
        'street': 'green',
        'tax_site': 24,
        'price': 300
    },
    {
        'type': 'property',
        'position': 32,
        'title': 'Oxford Street',
        'street': 'green',
        'tax_site': 26,
        'price': 300
    },
    {
        'type': 'property',
        'position': 34,
        'title': 'Bond Street',
        'street': 'green',
        'tax_site': 28,
        'price': 320
    },
    {
        'type': 'property',
        'position': 37,
        'title': 'Park Lane',
        'street': 'blue',
        'tax_site': 35,
        'price': 350
    },
    {
        'type': 'property',
        'position': 39,
        'title': 'Mayfair',
        'street': 'blue',
        'tax_site': 50,
        'price': 400
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
        'title': 'Maryll Boan Station',
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

squares = properties + utilities + specials
