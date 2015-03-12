# Test views and rules in the Monopoly application

from django.test import TestCase, Client
from monopoly.models import *
import rules

import json

def get_player(client):
    assert isinstance(client, Client), "To get a player you need a client"
    return Player.objects.get(session_id=client.session.session_key)

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
    
    def test_join_game(self):
        client = self.clients[0]
        client.get('/game/{0}/'.format(self.game1.id), follow=True)
        player = get_player(client)
        self.assertEquals(player.game, self.game1)

    def test_turn_initialisation(self):
        for client in self.clients:
            client.get('/game/{0}/'.format(self.game1.id), follow=True)
        
        expected_plays_in_turns = 1
        for client in self.clients:
            player = get_player(client)
            self.assertEquals(player.plays_in_turns, expected_plays_in_turns)
            expected_plays_in_turns += 1
        
    def test_join_different_game(self):
        client = self.clients[0]
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

    def test_turns(self):
        for client in self.clients:
            player = get_player(client)
            self.assertEquals(player.plays_in_turns, 0)
            client.get('/game/end_turn/')

    def test_end_turn_when_not_your_turn(self):
        turn = json.loads(self.clients[1].get('/game/end_turn/').content)
        self.assertFalse(turn["success"])
    
    def test_roll_when_your_turn(self):
        roll = json.loads(self.clients[0].get('/game/roll/').content)
        self.assertTrue(roll["success"])

    def test_roll_when_not_your_turn(self):
        roll = json.loads(self.clients[1].get('/game/roll/').content)
        self.assertFalse(roll["success"])

class TestBuying(TestGameFlow):
    def setUp(self):
        TestGameFlow.setUp(self)

    def test_buy_when_not_your_turn(self):
        buy = json.loads(self.clients[1].get('/game/buy/1/').content)
        self.assertFalse(buy["success"])

    def test_buy_property(self):
        buy = json.loads(self.clients[0].get('/game/buy/1/').content)
        self.assertTrue(buy["success"])

    def test_buy_utility(self):
        buy = json.loads(self.clients[0].get('/game/buy/5/').content)
        self.assertTrue(buy["success"])

    def test_buy_special(self):
        buy = json.loads(self.clients[0].get('/game/buy/0/').content)
        self.assertFalse(buy["success"])

    def test_buy_property_already_owned(self):
        self.clients[0].get('/game/buy/1/')
        buy = json.loads(self.clients[1].get('/game/buy/1/').content)
        self.assertFalse(buy["success"])

    def test_buy_utility_already_owned(self):
        client0 = self.clients[0]
        client1 = self.clients[1]
        client0.get('/game/buy/5/')
        buy = json.loads(client1.get('/game/buy/5/').content)
        self.assertFalse(buy["success"])

class TestPayRent(TestGameFlow):
    def setUp(self):
        TestGameFlow.setUp(self)

    def test_pay_rent_your_property(self):
        self.clients[0].get('/game/buy/1/')
        player = get_player(self.clients[0])
        money_before = player.money
        rules.move_player(player, (0,1))
        player = get_player(self.clients[0])
        self.assertEquals(player.money, money_before)

    def test_pay_rent_another_property(self):
        self.clients[0].get('/game/buy/1/')
        player = get_player(self.clients[1])
        money_before = player.money
        rules.move_player(player, (0,1))
        property = Square.objects.get(game=self.game, position=1).property
        player = get_player(self.clients[1])
        self.assertEquals(player.money, money_before - property.tax_site)

    def test_pay_rent_your_utility(self):
        self.clients[0].get('/game/buy/5/')
        player = get_player(self.clients[0])
        money_before = player.money
        rules.move_player(player, (0,5))
        player = get_player(self.clients[0])
        self.assertEquals(player.money, money_before)

    def test_pay_rent_another_utility(self):
        self.clients[0].get('/game/buy/5/')
        player = get_player(self.clients[1])
        money_before = player.money
        rules.move_player(player, (0,5))
        property = Square.objects.get(game=self.game, position=5).property
        player = get_player(self.clients[1])
        self.assertEquals(player.money, money_before - property.tax_site)
