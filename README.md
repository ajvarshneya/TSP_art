# TSP_art

Strategy:
1. Generate images:
	1. Convert images to grayscale images
	2. Use [StippleGen](https://github.com/evil-mad/stipplegen/releases/tag/v2.31) to create SVG of stippled grayscale images
2. Obtain list of points from stippled SVG
3. Solve TSP for given points, use heuristic strategy.
	MST --> graph --> DFS --> 2-opt --> ??? --> profit
4. Draw image
