# The Settings (s_settings) will control the ELO calculation with the following:
    #    - K-factor
    #    - E-factor
    #    - ELO Base
    #    - Multiplier
    #
    # The Distribution (t_distr) will control how many player for each game will receive points and also what
    # percentage of points each position should receive.
    #
    # The calculation will give points to all players receiving points from all players with less or equal position
    # (ties are possible). When a winning player receives points from a losing player then a standard ELO calculation
    # are done to calculate points given from winning player to losing player based on the player's current ratings.
    # (in case of a tie both players will give points to each other - with the lower rated player receiving the more
    # points). Once the ELO calculation points are ready between all players then these are adjusted based on the
    # discrepancy between the percentage points received when all player would have the same rating and the distribution
    # percentages
    #
    # Example:
    #
    # Current ratings: P1 = 1200, P2 = 1100, P3 = 1000, P4 = 900, P5 = 800, P6 = 700
    # Game results: 1st: P4, 2nd: P2 & P5
    # Settings: K-factor = 10, E-Factor = 400
    # Distribution: [2,1,100],[4,1,60],[4,2,30],[4,3,10],[8,1,50],[8,2,30],[8,4,10]
    #
    # Based on distribution in this example we have a player count of 6 and the first value in the distribution
    # represents 'Count From' so the one with count from 4 would be used. The second value in the distribution
    # represents 'Position To' so based on the highest among the 'Count From' 4 would be 3 'Position To', so 3
    # players will receive points from a player with less or equal position.
    #
    # Based on that we have a tie for 2nd place the distribution percentages should be the following:
    # 1st: 60%
    # 2nd: 20% (which is the average of the 2nd for 30% and 3rd for 10%)
    #
    # The following points would be calculated based on standard ELO calculation and the settings in the case of
    # all player would have the same ELO rating 1000 (base ELO rating)
    # P4<P1: 5, P4<P2: 5, P4<P3: 5, P4<P5: 5, P4<P6: 5
    # P2<P1: 5, P2<P3: 5, P2<P5: 5, P2<P6: 5
    # P5<P1: 5, P5<P2: 5, P5<P3: 5, P5<P6: 5
    #
    # P4 Total = 5 + 5 + 5 + 5 + 5 = 25
    # P2 Total = 5 + 5 + 5 + 5 - 5 = 15 (Note: P2 gains and looses points against P5 due to the tie)
    # P5 Total = 5 + 5 + 5 + 5 - 5 = 15 (Note: P5 gains and looses points against P2 due to the tie)
    #
    # Initial Point distribution: P4 = 45.45%, P2 = 27.27% and P5 = 27.27%
    # Distribution based on settings: P4 = 60%, P2 = 20%, P5 = 20%
    #
    # As you can see P4 should receive more points to match the Distribution based on Settings. Therefore these are
    # the adjustments that should be done for each position:
    # P4: ( 60 - 45.45 ) / 45.45 = 32%
    # P2: ( 20 - 27.27 ) / 27.27 = -26.7%
    # P2: ( 20 - 27.27 ) / 27.27 = -26.7%
    #
    # The following Points would be calculated based on standard ELO calculation and the Settings (in these
    # calculations I have rounded values to make it easier, in the program these values will have decimals)
    # P4<P1: 8, P4<P2: 8, P4<P3: 6, P4<P5: 4, P4<P6: 2
    # P2<P1: 6, P2<P3: 4, P2<P5: 2, P2<P6: 1
    # P5<P1: 9, P5<P2: 8, P5<P3: 8, P5<P6: 4
    #
    # P4 Total = 8 + 8 + 6 + 4 + 2 = 28
    # P2 Total = 6 + 4 + 2 + 1 - 8 = 5  (Note: P2 gains and looses points against P5 due to the tie)
    # P5 Total = 9 + 8 + 8 + 4 - 2 = 27 (Note: P5 gains and looses points against P2 due to the tie)
    #
    #