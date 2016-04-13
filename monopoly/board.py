# -*- encoding: UTF-8 -*-
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
        'title': 'Capite',
        'street': '#955335',
        'tax_site': 20,
        'price': 600,
        'house_price': 500
    },
    {
        'type': 'property',
        'position': 3,
        'title': 'Capitole',
        'street': '#955335',
        'tax_site': 40,
        'price': 600,
        'house_price': 500
    },
    {
        'type': 'property',
        'position': 6,
        'title': 'Stade de Copet 1',
        'street': '#AAE0FA',
        'tax_site': 60,
        'price': 1000,
        'house_price': 500
    },
    {
        'type': 'property',
        'position': 8,
        'title': 'Stade de Copet 2',
        'street': '#AAE0FA',
        'tax_site': 60,
        'price': 1000,
        'house_price': 500
    },
    {
        'type': 'property',
        'position': 9,
        'title': 'Stade de Copet 3',
        'street': '#AAE0FA',
        'tax_site': 80,
        'price': 1200,
        'house_price': 500
    },
    {
        'type': 'property',
        'position': 11,
        'title': 'Parc Chaplin',
        'street': '#D93A96',
        'tax_site': 100,
        'price': 1400,
        'house_price': 1000
    },
    {
        'type': 'property',
        'position': 13,
        'title': 'Jardin Roussy',
        'street': '#D93A96',
        'tax_site': 100,
        'price': 1400,
        'house_price': 1000
    },
    {
        'type': 'property',
        'position': 14,
        'title': 'Jardin Doret',
        'street': '#D93A96',
        'tax_site': 120,
        'price': 1600,
        'house_price': 1000
    },
    {
        'type': 'property',
        'position': 16,
        'title': 'Alimentarium',
        'street': '#F7941D',
        'tax_site': 140,
        'price': 1800,
        'house_price': 1000
    },
    {
        'type': 'property',
        'position': 18,
        'title': 'Musee de la photo',
        'street': '#F7941D',
        'tax_site': 140,
        'price': 1800,
        'house_price': 1000
    },
    {
        'type': 'property',
        'position': 19,
        'title': 'Place du marche',
        'street': '#F7941D',
        'tax_site': 160,
        'price': 2000,
        'house_price': 1000
    },
    {
        'type': 'property',
        'position': 21,
        'title': 'Boucherie Stuby',
        'street': '#ED1B24',
        'tax_site': 180,
        'price': 2200,
        'house_price': 1500
    },
    {
        'type': 'property',
        'position': 23,
        'title': 'Boucherie Matthey',
        'street': '#ED1B24',
        'tax_site': 180,
        'price': 2200,
        'house_price': 1500
    },
    {
        'type': 'property',
        'position': 24,
        'title': 'Boucherie Ruchet',
        'street': '#ED1B24',
        'tax_site': 200,
        'price': 2400,
        'house_price': 1500
    },
    {
        'type': 'property',
        'position': 26,
        'title': 'Le Veme',
        'street': '#FEF200',
        'tax_site': 220,
        'price': 2600,
        'house_price': 1500
    },
    {
        'type': 'property',
        'position': 27,
        'title': 'Le petit leman',
        'street': '#FEF200',
        'tax_site': 220,
        'price': 2600,
        'house_price': 1500
    },
    {
        'type': 'property',
        'position': 29,
        'title': 'LE BOUT DU MONDE',
        'street': '#FEF200',
        'tax_site': 240,
        'price': 2800,
        'house_price': 1500
    },
    {
        'type': 'property',
        'position': 31,
        'title': 'St-Martin',
        'street': '#1FB25A',
        'tax_site': 260,
        'price': 3000,
        'house_price': 2000
    },
    {
        'type': 'property',
        'position': 32,
        'title': 'Le Samaritain',
        'street': '#1FB25A',
        'tax_site': 260,
        'price': 3000,
        'house_price': 2000
    },
    {
        'type': 'property',
        'position': 34,
        'title': 'La nouvelle Villa-Gerard',
        'street': '#1FB25A',
        'tax_site': 280,
        'price': 3200,
        'house_price': 2000
    },
    {
        'type': 'property',
        'position': 37,
        'title': 'Manor',
        'street': '#0072BB',
        'tax_site': 350,
        'price': 3500,
        'house_price': 2000
    },
    {
        'type': 'property',
        'position': 39,
        'title': 'Nestle',
        'street': '#0072BB',
        'tax_site': 500,
        'price': 4000,
        'house_price': 2000
    }
]

utilities = [
    {
        'type': 'utility',
        'position': 5,
        'title': 'Gare de Vevey',
        'price': 2000,
        'tax_site': 250
    },
    {
        'type': 'utility',
        'position': 12,
        'title': 'Les ateliers mecaniques',
        'price': 1500,
        'tax_site': 250
    },
    {
        'type': 'utility',
        'position': 15,
        'title': 'La Tour de Peilz Gare',
        'price': 2000,
        'tax_site': 250
    },
    {
        'type': 'utility',
        'position': 25,
        'title': 'Vevey-Funi',
        'price': 2000,
        'tax_site': 250
    },
    {
        'type': 'utility',
        'position': 28,
        'title': 'STEP de Vevey',
        'price': 1500,
        'tax_site': 250
    },
    {
        'type': 'utility',
        'position': 35,
        'title': 'Blonay Gare',
        'price': 2000,
        'tax_site': 250
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
                'param': 2000
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
        'description': 'Dossier de camp termine ! Vas immediatement sur la case START',
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
        'name': 'Vent au marché',
        'description': 'Ton unite a fait une magnifique vente au marche ! En plus de faire plein de pub, tu gagnes 500$ .',
        'effect':
            {
                'type': 'give_money',
                'param': 500,
            }
    },
    {
        'name': 'ALERTE A LA DIARÉE !',
        'description': 'Tu attrapes la diaree en plein camp ! Va immediatement en quarantaine (prison)',
        'effect':
            {
                'type': 'go_to_jail',
                'param': 0,
            }
    },
    {
        'name': 'OUPS !',
        'description': 'Tu as oublie de payer ta cotisation annuelle ',
        'effect':
            {
                'type': 'take_money',
                'param': 250
            }
    }
]

squares = sorted(properties + utilities + specials, key=lambda s: s['position'])
