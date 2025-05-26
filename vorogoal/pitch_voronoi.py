import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
import matplotlib.patches as patches
import matplotlib.image as mpimg


class PitchVoronoi:
    def __init__(self, field_length=105, field_width=68, pitch_image_path=None):
        """
        Initialize the Voronoi diagram over a football pitch.
        :param field_length: Field length in meters (default 105)
        :param field_width: Field width in meters (default 68)
        :param pitch_image_path: Path to pitch image to use as background
        """
        self.field_length = field_length
        self.field_width = field_width
        self.pitch_image_path = pitch_image_path
        self.image = mpimg.imread(pitch_image_path) if pitch_image_path else None
        self.players = None
        self.colors = None

    def set_players(
        self, team1_coords, team2_coords, team1_color="#ff4444", team2_color="#3366ff"
    ):
        """
        Set player positions for two teams and assign their colors.
        :param team1_coords: List or array of shape (N, 2) for team 1 players
        :param team2_coords: List or array of shape (M, 2) for team 2 players
        :param team1_color: Color for team 1 zones (default red)
        :param team2_color: Color for team 2 zones (default blue)
        """
        team1 = np.array(team1_coords)
        team2 = np.array(team2_coords)
        self.players = np.vstack((team1, team2))
        self.colors = [team1_color] * len(team1) + [team2_color] * len(team2)

    def draw(self, show=True, save_path=None):
        """
        Draw the Voronoi diagram over the pitch image.
        :param show: Whether to show the plot window
        :param save_path: Optional path to save the image as file
        """
        if self.players is None or self.colors is None:
            raise ValueError("Please call set_players() first")

        fig, ax = plt.subplots(figsize=(12, 8))
        if self.image is not None:
            ax.imshow(self.image, extent=[0, self.field_length, 0, self.field_width])

        vor = Voronoi(self.players)
        pitch_bounds = Polygon(
            [
                (0, 0),
                (self.field_length, 0),
                (self.field_length, self.field_width),
                (0, self.field_width),
            ]
        )

        for idx, region_index in enumerate(vor.point_region):
            region = vor.regions[region_index]
            if not region or -1 in region:
                continue
            polygon = [vor.vertices[i] for i in region]
            poly = Polygon(polygon)
            clipped = poly.intersection(pitch_bounds)
            if not clipped.is_empty and clipped.geom_type == "Polygon":
                patch = patches.Polygon(
                    np.array(clipped.exterior.coords),
                    facecolor=self.colors[idx],
                    edgecolor="black",
                    linewidth=0.5,
                    alpha=0.4,
                )
                ax.add_patch(patch)

        ax.scatter(self.players[:, 0], self.players[:, 1], c=self.colors, s=60)
        ax.set_xlim(0, self.field_length)
        ax.set_ylim(0, self.field_width)
        ax.set_aspect("equal")
        ax.axis("off")
        plt.title("Voronoi Diagram over Football Pitch")

        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()
