# GUI toggle supports True or False
# if True, we will be running the system client from a GUI. From the GUI, the user can select strategies to run,
# see system health report in runtime from different GUI tabs for each client, and see the results of the strategies in the GUI.
# If False, we will be running the system client from terminal. If running from a VM or cluster, we will be running from terminal so this should be set to False.
GUI_enabled = False

# Direct_Trade_enabled toggle supports True or False
# if True, we will be running the system client to directly trade on the market. This can be
# used to trade on trading adapters like IBKR and Alpaca.
# If False, we will be using the system client to return the results of the strategy. 
# If we are running other models and want Hyper model to be used with other models and fit into the entire architecture, direct trade
# should be set to False.
Direct_Trade_enabled = False