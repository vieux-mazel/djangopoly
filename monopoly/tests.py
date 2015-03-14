# A mix of white box and black box tests for testing
# views in the monopoly application.
#
# These are used in conjuction with assertions for things
# that should never, ever fail in the source code.

from django.test import TestCase, Client
from monopoly.models import *
import rules

import json

# Extend Django's Client class to be able to get the Player
# it corresponds to.
class Client(Client):
    def player(self):
        return Player.objects.get(session_id=self.session.session_key)


class TestIndex(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)


class TestGameCreation(TestCase):
    def setUp(self):
        self.client = Client()

    def test_game_creation_public(self):
        self.client.get('/new_game/public', follow=True)
        self.assertFalse(Game.objects.all()[0].private)

    def test_game_creation_private(self):
        self.client.get('/new_game/private', follow=True)
        self.assertTrue(Game.objects.all()[0].private)

    def test_game_creation(self):
        self.client.get('/new_game/public', follow=True)
        self.assertEquals(Game.objects.all().count(), 1) # One game created
        game = Game.objects.all()[0]
        self.assertEquals(game.square_set.count(), 40) # There should be 40 squares in the game

    def test_game_start(self):
        self.client.get('/new_game/public', follow=True)
        game = Game.objects.all()[0]
        self.client.get('/game/{0}/start/'.format(game.id))
        self.assertTrue(Game.objects.all()[0].in_progress)


class TestGameJoin(TestCase):
    def setUp(self):
        Client().get('/new_game/public', follow=True)
        Client().get('/new_game/public', follow=True)
        self.game1 = Game.objects.all()[0]
        self.game2 = Game.objects.all()[1]
        self.clients = []
        for i in range(4):
            self.clients.append(Client())
        # Named clients
        self.john = self.clients[0]
        self.mary = self.clients[1]
    
    def test_join_game(self):
        client = self.john
        client.get('/game/{0}/'.format(self.game1.id), follow=True)
        player = client.player()
        self.assertEquals(player.game, self.game1)

    def test_turn_initialisation(self):
        for client in self.clients:
            client.get('/game/{0}/'.format(self.game1.id), follow=True)
        
        expected_plays_in_turns = 1
        for client in self.clients:
            player = client.player()
            self.assertEquals(player.plays_in_turns, expected_plays_in_turns)
            expected_plays_in_turns += 1
        
    def test_join_different_game(self):
        client = self.john
        client.get('/game/{0}/'.format(self.game1.id), follow=True)
        response = client.get('/game/{0}/'.format(self.game2.id), follow=True)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)


class TestGameFlow(TestCase):
    def setUp(self):
        Client().get('/new_game/public', follow=True)
        self.game = Game.objects.all()[0]
        self.game.player_set.all().delete() # Remove the anonymous player that just created the game
        self.clients = []
        for i in range(4):
            client = Client()
            client.get('/game/{0}/'.format(self.game.id), follow=True)
            self.clients.append(client)
        # Named clients
        self.john = self.clients[0]
        self.mary = self.clients[1]

    def test_turns(self):
        for client in self.clients:
            player = client.player()
            self.assertEquals(player.plays_in_turns, 0)
            client.get('/game/end_turn/')

    def test_end_turn_when_not_your_turn(self):
        turn = json.loads(self.mary.get('/game/end_turn/').content)
        self.assertFalse(turn["success"])
    
    def test_roll_when_your_turn(self):
        roll = json.loads(self.john.get('/game/roll/').content)
        self.assertTrue(roll["success"])

    def test_roll_when_not_your_turn(self):
        roll = json.loads(self.mary.get('/game/roll/').content)
        self.assertFalse(roll["success"])


class TestBuying(TestGameFlow):
    def setUp(self):
        TestGameFlow.setUp(self)

    def test_buy_when_not_your_turn(self):
        buy = json.loads(self.mary.get('/game/buy/1/').content)
        self.assertFalse(buy["success"])

    def test_buy_property(self):
        buy = json.loads(self.john.get('/game/buy/1/').content)
        self.assertTrue(buy["success"])

    def test_buy_utility(self):
        buy = json.loads(self.john.get('/game/buy/5/').content)
        self.assertTrue(buy["success"])

    def test_buy_special(self):
        buy = json.loads(self.john.get('/game/buy/0/').content)
        self.assertFalse(buy["success"])

    def test_buy_property_twice(self):
        self.john.get('/game/buy/1/')
        buy = json.loads(self.john.get('/game/buy/1/').content)
        self.assertFalse(buy["success"])

    def test_buy_property_already_owned(self):
        self.john.get('/game/buy/1/')
        self.john.get('/game/end_turn/')
        buy = json.loads(self.mary.get('/game/buy/1/').content)
        self.assertFalse(buy["success"])

    def test_buy_utility_already_owned(self):
        self.john.get('/game/buy/5/')
        self.john.get('/game/end_turn/')
        buy = json.loads(self.mary.get('/game/buy/5/').content)
        self.assertFalse(buy["success"])

    def test_buy_property_street_conflict(self):
        self.john.get('/game/buy/1/')
        self.john.get('/game/end_turn/')
        buy = json.loads(self.mary.get('/game/buy/3/').content)
        self.assertFalse(buy["success"])


class TestPayRent(TestGameFlow):
    def setUp(self):
        TestGameFlow.setUp(self)

    # Sets a property/utility as bought without
    # going through the API.
    def set_bought(self, client, identity):
        identity.owned_by = client.player()
        identity.save()

    def test_pay_rent_your_property(self):
        self.set_bought(self.john, Square.objects.get(game=self.game, position=1).property)
        money_before = self.john.player().money
        rules.move_player(self.john.player(), (0,1))
        self.assertEquals(self.john.player().money, money_before)

    def test_pay_rent_another_property(self):
        property = Square.objects.get(game=self.game, position=1).property
        self.set_bought(self.john, property)
        money_before = self.mary.player().money
        rules.move_player(self.mary.player(), (0,1))
        self.assertEquals(self.mary.player().money, money_before - property.tax_site)

    def test_pay_rent_your_utility(self):
        self.set_bought(self.john, Square.objects.get(game=self.game, position=5).utility)
        money_before = self.john.player().money
        rules.move_player(self.john.player(), (0,5))
        self.assertEquals(self.john.player().money, money_before)

    def test_pay_rent_another_utility(self):
        utility = Square.objects.get(game=self.game, position=5).utility
        self.set_bought(self.john, utility)
        money_before = self.mary.player().money
        rules.move_player(self.mary.player(), (0,5))
        self.assertEquals(self.mary.player().money, money_before - utility.tax_site)

    def test_pay_rent_multiple_utilities(self):
        self.set_bought(self.john, Square.objects.get(game=self.game, position=5).utility)
        self.set_bought(self.john, Square.objects.get(game=self.game, position=12).utility)
        self.set_bought(self.john, Square.objects.get(game=self.game, position=15).utility)
        money_before = self.mary.player().money
        rules.move_player(self.mary.player(), (0,5))
        utility = Square.objects.get(game=self.game, position=5).utility
        self.assertEquals(self.mary.player().money, money_before - utility.tax_site * 3)


class TestJail(TestCase):
    def setUp(self):
        Client().get('/new_game/public', follow=True)
        self.game = Game.objects.all()[0]
        self.game.player_set.all().delete() # Delete dummy player that created the game
        self.john = Client()
        self.john.get('/game/{0}/'.format(self.game.id), follow=True)
        self.money_before = self.john.player().money
        rules.move_player(self.john.player(), (30, 0)) # Roll a 30 to land on "Go to jail"

    def test_go_to_jail(self):
        self.assertEquals(self.john.player().square.position, 10) # Should have been moved to position 10, "Jail"
    
    def test_jail_stay_for_three_turns(self):
        for t in range(3):
            self.assertTrue(self.john.player().is_in_jail())
            rules.move_player(self.john.player(), (3, 5))
        self.assertFalse(self.john.player().is_in_jail())
        self.assertEquals(self.john.player().money, self.money_before - 50)

    def test_jail_liberate_by_bailout(self):
        bailout = json.loads(self.john.get('/game/pay_bailout/').content)
        self.assertTrue(bailout["success"])
        self.assertEquals(self.john.player().money, self.money_before - 50)
        self.assertFalse(self.john.player().is_in_jail())

    def test_jail_liberate_by_dice(self):
        rules.move_player(self.john.player(), (1, 1))
        self.assertFalse(self.john.player().is_in_jail())
        self.assertEquals(self.john.player().money, self.money_before)


