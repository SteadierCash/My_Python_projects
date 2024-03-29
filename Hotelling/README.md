# Hotelling Model
The Hotelling model, also known as the Hotelling's linear city model, is an economic theory that describes spatial competition between firms. It posits that firms located along a linear market or spatial continuum will strategically position themselves to maximize market share and profit. In this model, firms choose their locations sequentially along the linear market, considering factors such as consumer preferences, transportation costs, and competitors' locations. Hotelling's model is commonly used to analyze scenarios such as product differentiation, pricing strategies, and spatial equilibrium in markets.

# Algorithm Description

The algorithm operates based on the following steps:

1. **Randomly select positions of players, prices, and product qualities for all players.**
2. **Calculate player payouts.**
3. **Attempt to randomly select a configuration resulting in a better payout for player 1.** For different attempts, the algorithm tries to change other values:
   - Attempts [1, 1000): changing the price,
   - Attempts [1000, 2000): changing the quality and price,
   - Attempts [2000, 3000): changing the position,
   - Attempts from 3000: changing the entire configuration.
4. **Check if the payout is better than the current one:**
   - If yes, accept the position as the new better position.
   - If no, attempt to find a better position again.
5. **Repeat steps 3 and 4 for the remaining players.**

## Player Class

To ensure the efficient operation of the described algorithm, a class named `Player` has been created to store all necessary information about the players. The arguments required to create the class are:

- `player number`: a unique identifier for each player.
- `place`: their current position.
- `price`: the current price of their product.
- `quality`: the current quality of their products.
  
### Functions for Algorithm Operation
The algorithm operates by randomly selecting new settings for players each time. Therefore, functions facilitating the class's operation have been added:
 #### `calculate_cost`
- Description: a function to calculate the cost of purchasing the product from player j for client i. It is defined as:

$$
c_{ij}(place_j, price_j, quality_j) = \left(\frac{|i - place_j| + 1}{100}\right)^2 \cdot 0.4 + \left(\frac{price_j}{10}\right)^2 \cdot 0.4 - \left(\frac{quality_j}{10}\right)^2 \cdot 0.2
$$

where:
- `i` is the position of the i-th client for which we calculate the cost,
- `place_j` is the position of the j-th player,
- `price_j` is the price of the product chosen by the j-th player,
- `quality_j` is the quality of the product chosen by the j-th player.

- Arguments:
   `i` is the position of the i-th client for which we calculate the cost
#### **new_place**
- Description: Calculates a new position for a given player.
- Arguments:
  - `iteration`: The current iteration number, representing the attempt to find a better position for the player.
  - `l`: The length of the market.
- Functionality: Adjusts the player's position based on the current iteration and market length.

#### **new_price**
- Description: Determines a new price for a given player.
- Arguments:
  - `iteration`: The current iteration number, representing the attempt to find a better price for the player.
- Functionality: Similar to `new_place`, but does not take the market length into account. The width coefficient of the interval is set to 4.

#### **new_quality**
- Description: Calculates a new quality for a given player.
- Arguments:
  - `iteration`: The current iteration number, representing the attempt to find a better quality for the player.
- Functionality: Similar to `new_price`, but the iterator value is consistently decreased by 999. This function is called only after 1000 attempts.

#### **copy**
- Description: Copies certain player information during the search for a better position.
- Functionality: Used to duplicate player information when searching for a better position.

#### **write**
- Description: Outputs selected player information.
- Functionality: Used to print specific player details.
