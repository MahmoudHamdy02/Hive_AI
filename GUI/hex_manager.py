from typing import List, Tuple
from hex import HexagonTile, HexagonOutline

class HexManager:
    """ Class for managing and rendering hexagon tiles"""
    
    def __init__(self, origin: Tuple[float, float], radius: float, minimal_radius: float):
        self.origin: float = origin
        self.radius: float = radius
        self.minimal_radius: float = minimal_radius
        self.hexagons: List[HexagonTile] = []
        self.outlines: List[HexagonOutline] = []

    def __axialToPixels(self, x: int, y: int) -> Tuple[float, float]:
        """ Convert axial coordinates (q,r) to cartesian coordinates (x, y)"""
        return (
            2 * self.minimal_radius * x  + self.minimal_radius * y, 
            self.radius * (3./2 * y)
        )
    
    def createHexagonTile(self, q: int, r: int, insect = None, color = None) -> HexagonTile:
        """ 
            Creates and renders a new hexagon at (q,r).\n
            Returns the created hexagon.\n
            Throws an error if a tile or outline already exists in the provided position.
        """
        top_z = 0
        # If new piece is not a beetle, throw an error if a piece already exists at that position
        if insect != "beetle":
            for hexagon in self.hexagons:
                if hexagon.axial_coordinates == (q, r):
                    raise Exception("Tile already exists at specified axial coordinates")
        # If it is a beetle, get the z of the top tile 
        else:
            tiles_at_position: List[HexagonTile] = []
            for hexagon in self.hexagons:
                if hexagon.axial_coordinates == (q, r):
                    tiles_at_position.append(hexagon)
            if len(tiles_at_position) > 0:
                for tile in tiles_at_position:
                    if tile.z > top_z:
                        top_z = tile.z
                top_z = top_z + 1

        pixels = self.__axialToPixels(q, r)
        position = (self.origin[0]+pixels[0], self.origin[1]+pixels[1])
        hexagon = HexagonTile((q,r), position, insect, color, top_z)
        self.hexagons.append(hexagon)
        return hexagon

    def removeHexagonTile(self, q: int, r: int) -> HexagonTile:
        """ 
            Deletes a hexagon at (q,r).\n
            Returns the deleted hexagon.\n
            Throws an error if no tile exists in the provided position.
        """
        tiles_at_position: List[HexagonTile] = []
        for hexagon in self.hexagons:
            if hexagon.axial_coordinates == (q, r):
                tiles_at_position.append(hexagon)
        if len(tiles_at_position) == 0:
            raise Exception("No tile exists at specified axial coordinates")
        top_tile = tiles_at_position[0]
        for tile in tiles_at_position:
            if tile.z > top_tile.z:
                top_tile = tile
        self.hexagons.remove(top_tile)
        return top_tile

    def drawOutline(self, q: int, r: int) -> HexagonOutline:
        """ 
            Draws a hexagon outline at (q,r).\n
            Returns the created outline.\n
            Throws an error if a tile or outline already exists in the provided position
        """
        # Can be drawn on top of tiles
        for outline in self.outlines:
            if outline.axial_coordinates == (q, r):
                raise Exception("Outline already exists at specified axial coordinates"+str(q)+" "+str(r)+" ")

        pixels = self.__axialToPixels(q, r)
        position = (self.origin[0]+pixels[0], self.origin[1]+pixels[1])
        outline = HexagonOutline((q,r), position)
        self.outlines.append(outline)
        return outline

    def removeOutline(self, q: int, r: int) -> HexagonOutline:
        """ 
            Deletes an outline at (q,r).\n
            Returns the deleted outline.\n
            Throws an error if no outline exists in the provided position.
        """
        for outline in self.outlines:
            if outline.axial_coordinates == (q, r):
                self.outlines.remove(outline)
                return outline
        raise Exception("No outline exists at specified axial coordinates")
    def removeAllOutlines(self) -> None:
        self.outlines = []
    def getTile(self, q: int, r: int) -> HexagonTile | None: 
        """ Returns the tile at the specified position if exists, otherwise returns None"""
        for hexagon in self.hexagons:
            if hexagon.axial_coordinates == (q, r):
                return hexagon
        return None

    def render(self, screen) -> None:
        # Render outlines last so they are not hidden under tiles
        for hexagon in self.hexagons:
            hexagon.render(screen)
        for outline in self.outlines:
            outline.render(screen)
