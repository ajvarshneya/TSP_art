# TSP_art

1. Generate images:
	- Convert images to grayscale images
	- Use [StippleGen](https://github.com/evil-mad/stipplegen/releases/tag/v2.31) to create SVG of stippled grayscale images
2. Obtain list of points from stippled SVG
3. Solve TSP for given points, use heuristic strategy:
  - Find MST
  - Create Eulerian Graph
  - Find shortest path using Eulerian Graph
4. Draw image
