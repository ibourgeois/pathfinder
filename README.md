# Pathfinder

The purpose of this project is to find the shortest path through given set of points. It uses the brute force solution of TSP (traveling salesman problem) to solve this task. The complexity of this approach is O(n!), therefore, in further versions, I plan to implement some other algorithms in order to solve the problem more effectively.

## Usage
1. Create `.env` file in the working directory of this project.
2. Add the `API_KEY` variable to this file. You can generate your own api key at https://openrouteservice.org/.
3. Create a set of points, export the set as gpx and save it as `export.gpx` in the `input` directory.
4. Run the program: `python main.py`.
5. You will find the result as a gpx file in the `output` directory.

## Notes
- This program uses the openrouteservice API. You have to generate an API key in order to make this program work.
- The output of the openrouteservice API is only pure route. The waypoints are added manually from the input file.
