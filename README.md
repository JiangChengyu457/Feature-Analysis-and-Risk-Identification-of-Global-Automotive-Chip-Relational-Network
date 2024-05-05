# Feature-Analysis-and-Risk-Identification-of-Global-Automotive-Chip-Relational-Network

The background of this thesis is the automotive chip crisis that broke out in 2020. The dataset was built based on the stock price data of 42 leading companies in the chip industry from 2017 to 2021 for 5 years. The thesis then establishes 5 chip relational networks with DY spillover index matrix as the weight matrix and top companies as the model nodes, and then filtered. Node-level and Network-level feature analysis is tehn conducted, including k_core, degree_centrality, pagerank, betweeness_centrality, closeness_centrality, coefficient, average shortest path length, average clustering coefficient, and Louvain community discovery etc.

Conclusion of the thesis: The market distribution of the chip industry conforms to the "Pareto law", with high market concentration and stable competitive landscape. The global division of labor in the industrial chain is significant, and the supply chain layout is concentrated and single, with a fragile "radiating" characteristic. The possibility of material flow or information exchange interruption is high. And based on this, countermeasures and suggestions were proposed.

Attached file description:  
"cal_node.pdf" : the calculation results of node-level indexes.  
"cal_network.pdf" : the calculation results of network-level indexes.  
"analysis by synthesis method.pdf" : the fusion of indexes by the synthesis method.  
"build_graph + cal_index.py" : the code of building the network of every year, calculating indexes and conducting Louvain community discovery.
