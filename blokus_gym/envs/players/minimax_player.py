import numpy as np
from sys import maxsize
from blokus_gym.envs.players.player import Player
import copy


class MinimaxPlayer(Player):

    def score_player(self, game):
        score = 0
        for player in game.players:
            score_player = len(player.corners) + 5 * player.score
            score = score + score_player if player.index == self.index else score - score_player
        return score

    @staticmethod
    def play_without_do_move(game, move):
        if game.winners() is None:
            current = game.players[0]
            # print("Current player: " + current.name)
            proposal = move
            if proposal is None:
                # move on to next player, increment rounds
                first = game.players.pop(0)
                game.players = game.players + [first]
                game.rounds += 1
            # ensure that the proposed move is valid
            elif game.valid_move(current, proposal):
                # update the board with the move
                game.board.update(current, proposal)
                # let the player update itself accordingly
                current.update_player(proposal, game.board)
                # remove the piece that was played from the player
                current.remove_piece(proposal)
                # place the player at the back of the queue
                first = game.players.pop(0)
                game.players = game.players + [first]
                # increment the number of rounds just played
                game.rounds += 1

    def minimax(self, game, depth, prev_move):
        player = game.next_player()
        possible_moves = [move for move in player.possible_moves_opt() if self.game.valid_move(self, move)]
        if depth < 0 or len(possible_moves) == 0:
            return (self.score_player(game), prev_move)

        if player.index == self.index:
            score_move = (- maxsize - 1, None)
            for move in possible_moves:
                node = copy.deepcopy(player.game)
                MinimaxPlayer.play_without_do_move(node, move)
                score_move = max(score_move, self.minimax(node, depth - 1, move))
            return score_move
        else:
            score_move = (maxsize, None)
            for move in possible_moves:
                node = copy.deepcopy(player.game)
                MinimaxPlayer.play_without_do_move(node, move)
                score_move = min(score_move, self.minimax(node, depth - 1, move))
            return score_move

    def do_move(self):
        return self.minimax(copy.deepcopy(self.game), 1, None)[1]
