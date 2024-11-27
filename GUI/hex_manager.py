from typing import List, Tuple
from hex import HexagonTile

class HexManager:
    """ Class for managing and rendering hexagon tiles"""
    
    def __init__(self, origin: Tuple[float, float], radius: float, minimal_radius: float):
        self.origin: float = origin
        self.radius: float = radius
        self.minimal_radius: float = minimal_radius
        self.hexagons: List[HexagonTile] = []

    def __axialToPixels(self, x: int, y: int) -> Tuple[float, float]:
        """ Convert axial coordinates (q,r) to cartesian coordinates (x, y)"""
        return (
            2 * self.minimal_radius * x  + self.minimal_radius * y, 
            self.radius * (3./2 * y)
        )
    
    def createHexagonTile(self, q, r) -> HexagonTile:
        """ 
            Creates and renders a new hexagon at (q,r).\n
            Returns the created hexagon.\n
            Throws an error if a tile or outline already exists in the provided position.
        """
        pixels = self.__axialToPixels(q, r)
        position = (self.origin[0]+pixels[0], self.origin[1]+pixels[1])
        hexagon = HexagonTile(position)
        self.hexagons.append(hexagon)
        return hexagon

    def removeHexagonTile(self, q, r):
        """ 
            Deletes a hexagon at (q,r).\n
            Returns the deleted hexagon.\n
            Throws an error if no tile exists in the provided position.
        """
        pass

    def drawOutline(self):
        """ Draws a hexagon outline at (q,r). Throws an error if a tile or outline already exists in the provided position"""
        pass

    def removeOutline(self):
        """ Deletes a hexagon outline at (q,r). Throws an error if no outline exists in the provided position"""
        pass

    def render(self, screen):
        for hexagon in self.hexagons:
            hexagon.render(screen)
