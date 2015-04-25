# TSP_art

1. Generate images:
	1. Convert images to grayscale images
	2. Use [StippleGen](https://github.com/evil-mad/stipplegen/releases/tag/v2.31) to create SVG of stippled grayscale images
2. Obtain list of points from stippled SVG
3. Solve TSP for given points, use heuristic strategy:
  	1. Find MST
  	2. Create Eulerian Graph
  	3. Find shortest path using Eulerian Graph
4. Draw image
