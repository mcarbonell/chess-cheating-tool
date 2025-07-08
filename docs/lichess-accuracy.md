# How is accuracy calculated?

Accuracy is a measurement of how well you played in a game of chess. It is calculated by comparing your moves to the moves that a chess engine would have made.

We start by finding the single move that the engine thinks is best. Any move that is just as good as this best move is considered a "best" move. These are the moves that you would want to make.

Every other move is a mistake. The severity of the mistake depends on how much it changes the outcome of the game. A small mistake might change the win percentage by only a few points. A big mistake might change a winning position into a losing one.

We have a formula that takes the change in win percentage and converts it into a single number that represents the centipawn loss. This formula is:

`centipawn_loss = 2.9056 * log(win_percentage_before / win_percentage_after - 1) + 6.804`

This formula is a bit complicated, but it is designed to give a good measure of how bad a mistake is. The higher the centipawn loss, the worse the mistake.

Finally, we take all of your centipawn losses and average them together. This gives us your average centipawn loss for the game. We can then use this to calculate your accuracy percentage.

`accuracy = 103.1668 * exp(-0.04354 * average_centipawn_loss)`

This formula is also a bit complicated, but it is designed to give a good measure of how well you played. The higher the accuracy percentage, the better you played.
