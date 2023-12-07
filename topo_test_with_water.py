import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter

class Terrain:
    def __init__(self, size=1000):
        self.size = size
        self.heightmap = None
        self.custom_cmap = self.create_custom_colormap()

    def create_custom_colormap(self):
        terrain_cmap = plt.cm.get_cmap('terrain', 256)
        newcolors = terrain_cmap(np.linspace(0, 1, 256))
        blue = np.array([0, 0, 1, 0.4])  # RGBA for blue
        newcolors[:int(256/3), :] = blue # anything from 0 to 256 / 3 is blue
        return mcolors.ListedColormap(newcolors)

    def apply_gaussian_filter(self, sigma, weight):
        filtered_heightmap = gaussian_filter(np.random.rand(self.size, self.size) * 2, sigma=sigma)
        if self.heightmap is None:
            self.heightmap = filtered_heightmap * weight
        else:
            self.heightmap += filtered_heightmap * weight

    def display_contours(self):
        plt.figure(figsize=(10, 8))
        contour = plt.contourf(self.heightmap, cmap=self.custom_cmap, levels=20)
        plt.colorbar(contour)
        lines = plt.contour(self.heightmap, colors='black', linewidths=0.5, levels=20)
        plt.clabel(lines, inline=True, fontsize=8, fmt='%1.1f')
        plt.title("Contoured Heightmap with Water Representation")
        plt.show()
    
    def apply_hydration_erosion(self, erosion_strength=0.001, iterations=1, water_travel_distance = 1):
        #TODO fix local optimums
        """
        Simulates erosion by water flow over the terrain, with each water droplet
        performing a random walk to mimic natural erosion paths.
# 
        Parameters:
        erosion_strength: The initial amount by which the terrain is lowered during each erosion step.
        max_depth: Maximum depth allowed for erosion at a point in a single iteration.
        iterations: number of iterations a random walk is allowed to walk
        evaporation_chance: Chance a random walk stops
        """

        for iteration in range(iterations) : 
            water_tuple_list = []
            for i in range(self.size):
                for j in range(self.size):  
                    water_tuple_list.append((i, j))
            #creates a list of tuples that are spread acorss the size of the terrain
            #erode walk each water_tuple of water_tuple_list
            for water_tuple in water_tuple_list :
                for distance in range(water_travel_distance) :
                    next_water_tuple = self.get_lowest_adjacent_point(water_tuple[0], water_tuple[1])

                    erosion = self.heightmap[next_water_tuple[0],next_water_tuple[1]] - erosion_strength
                    print(erosion)
                    if erosion < 0 :
                        break # bottom of terrain reached
                    self.heightmap[next_water_tuple[0],next_water_tuple[1]] -= erosion # erode the next height
                    water_tuple = next_water_tuple
    
    def normalize_heightmap(self):
        self.heightmap = (self.heightmap - np.min(self.heightmap)) / (np.max(self.heightmap) - np.min(self.heightmap))

    def _get_lowest_adjacent_point(self, x, y):
        lowest_point = (x, y)
        lowest_height = self.heightmap[x, y]
        for dx in [-3,-2,-1, 0, 1,2,3,3]:
            for dy in [-3,-2,-1, 0, 1,2,3]:
                nx, ny = x + dx, y + dy
                # Skip the current point
                if nx == x and ny == y: # if point is the same
                    continue
                if self.is_outside_map(nx, ny): # if point is outside of map
                    continue
                if self.heightmap[nx, ny] < lowest_height:
                    lowest_height = self.heightmap[nx, ny]
                    lowest_point = (nx, ny)
        return lowest_point

    def _is_outside_map(self, x, y):
        return x < 0 or y < 0 or x >= self.size or y >= self.size

# Usage
terrain = Terrain(400)
terrain.apply_gaussian_filter(sigma=30, weight=0.8)  # High sigma for rolling hills
terrain.apply_gaussian_filter(sigma=15, weight=0.2)  # Lower sigma for variation
terrain.normalize_heightmap()  # Normalize heightmap to span from 0 to 1

terrain.display_contours()
terrain.apply_hydration_erosion()
terrain.display_contours()