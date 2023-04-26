# Pathfinder

This program performs the computation of the travelling salesman problem on a given set of GPS points. So far, the computation is implemented using brute force and nearest neighbor method.

## Usage

1. Create `.env` file in the working directory of this project.
2. Add the `API_KEY` variable to this file. You can generate your own api key at [https://openrouteservice.org](https://openrouteservice.org/).
3. Create a set of gps points, export the set as .gpx file and save it in the `input` directory.
4. Run the program: `python main.py`.
5. Follow the instructions in the GUI.
6. You will find the result as a .gpx file in the `output` directory.

## Docker Usage

Build the image:

```bash
docker build -t pathfinder .
```

Run the container:

```bash
docker run -it --rm -e API_KEY=<your_api_key> -v ${pwd}/input:/app/input -v ${pwd}/output:/app/output pathfinder
```

> Note: Replace `<your_api_key>` with your API key, which you can generate your own at [https://openrouteservice.org](https://openrouteservice.org/).

## Notes

- This program uses the openrouteservice API. You have to generate an API key in order to make this program work.
- The output of the openrouteservice API is only pure route. The waypoints are added manually from the input file.

## Background

Whenever I traveled to a city, I always found a few places I wanted to visit. Then I needed to find the optimal route that I could take to visit all those places. That's how the idea for this project was born.

I found an API to calculate distances between GPS points. Then I implemented a simple solution using brute force method. After that, I decided to add a GUI to practice working with the PyQt5 library. Then I added a graphical representation of the calculation and the resulting path. This was followed by an extension to perform the shortest path calculation using the nearest neighbor method, which was also the first solution method I thought of.

The next steps are, for example, to implement other methods to solve the TSP or to represent the solution directly in the integrated map.
