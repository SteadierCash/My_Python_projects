### The algorithm operates based on the following steps:

1. Randomly select positions of players, prices, and product qualities for all players.
2. Calculate player payouts.
3. Attempt to randomly select a configuration resulting in a better payout for player 1. For different attempts, the algorithm tries to change other values:
   - Attempts [1, 1000): changing the price,
   - Attempts [1000, 2000): changing the quality and price,
   - Attempts [2000, 3000): changing the position,
   - Attempts from 3000: changing the entire configuration.
4. Check if the payout is better than the current one:
   - If yes, accept the position as the new better position.
   - If no, attempt to find a better position again.
5. Repeat steps 3 and 4 for the remaining players.

 To ensure the efficient operation of the described algorithm, a class named `Player` has been created to store all necessary information about the players. The arguments required to create the class are:

- `player number`: a unique identifier for each player.
- `place`: their current position.
- `price`: the current price of their product.
- `quality`: the current quality of their products.

The algorithm operates by randomly selecting new settings for players each time. Therefore, functions facilitating the class's operation have been added:

- `calculate_cost`: a function to calculate the cost of purchasing the product from player j for client i. It is defined as:
  $$c_{ij}(place_j, price_j, quality_j) = \left (\displaystyle\frac{|i - place_j| + 1}{100}\right)^2 \cdot 0.4
+ \left (\displaystyle\frac{price_j}{10}\right) ^ 2 \cdot 0.4
- \left (\displaystyle\frac{quality_j}{10}\right) ^ 2 \cdot 0.2,$$

  where:
- `i` is the position of the i-th client for which we calculate the cost,
- `place_j` is the position of the j-th player,
- `price_j` is the price of the product chosen by the j-th player,
- `quality_j` is the quality of the product chosen by the j-th player.

