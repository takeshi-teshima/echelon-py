import importlib
import numpy as np
import pandas as pd
import geopandas as gpd  # For reading shapefiles.
import libpysal  # For constructing "Queen" neighborhoods.
from matplotlib.colors import to_rgba

# Type hinting
from typing import Optional
from echelon.api.base import Result_EchelonHotspot

required_modules = [gpd, libpysal]


class GISPlotter:
    def __init__(self, gdf: gpd.GeoDataFrame, name_col:Optional[str]=None):
        self.gdf = gdf
        self.name_col = name_col

    def plot_values(self, value_col: str, value_transform: Optional[callable]=None):
        from matplotlib.colors import to_rgba
        if value_transform is None:
            value_transform = lambda x: x
        color = self.gdf[value_col].map(lambda v: to_rgba('red', alpha=value_transform(v)))
        ax = self.gdf.plot(color=color, edgecolor='black')
        self._maybe_plot_names(ax)
        return ax

    def plot_hotspot(self, hotspots: Result_EchelonHotspot, label_col: str, nth:int=1, id_col: Optional[str]=None):
        """
        Parameters:
            nth: How-many-th hot spot to plot.
            id_col: the column containing the IDs that appear in the hot-spot detection results.
        """
        if id_col is None:
            id_col = self.name_col
        _df = self.gdf.assign(is_hotspot=self.gdf[id_col].isin(hotspots.iloc[nth - 1]['spot']))
        transform = lambda s: {True: to_rgba('black', alpha=0.3), False: to_rgba('white')}[s]
        return self._plot_labeled_map('is_hotspot', _df, transform)

    def _set_coords(self, c):
        if 'coords' in c:
            return
        c['coords'] = c['geometry'].apply(lambda x: x.representative_point().coords[:])
        c['coords'] = [coords[0] for coords in c['coords']]

    def _plot_labeled_map(self, value_col: str, gdf: Optional[gpd.GeoDataFrame]=None, value_transform: Optional[callable]=None):
        if value_transform is None:
            value_transform = lambda x: x

        c = gdf if gdf is not None else self.gdf

        ## Coloring
        ax = c.plot(
            color=c[value_col].map(value_transform),
            edgecolor='black',
            figsize=(10, 10))

        self._maybe_plot_names(ax, c)
        return ax

    def _maybe_plot_names(self, ax, c=None):
        if self.name_col is None:
            return
        c = c if c is not None else self.gdf
        self._set_coords(c)

        ## Assign names
        for _, row in c.iterrows():
            ax.text(row.coords[0], row.coords[1],
                    s=row[self.name_col],
                    horizontalalignment='center',
                    bbox={'facecolor': 'white', 'alpha':1, 'pad': 2, 'edgecolor':'none'})


class GISAdjacency:
    def __init__(self, gdf, adjacency_type:str='Queen', id_colname:Optional[str]=None):
        """
        Parameters:
            adjacency_type : the name of the adjacency type (the name is used to import a submodule from ``libpysal.weights``).
        Notes:
            The default ``adjacency_type='Queen'`` means using "Queen" adjacency graph.
            Two polygons are connected if they share a single point on their boundary
            (analogously to the "Moore" neighborhood).
        """
        self.gdf = gdf
        self.adjacency_type = adjacency_type
        self.adj = self._build_adjacency(gdf)
        self.id_colname = id_colname

    def _build_series(self):
        adj_series = (self.adj.to_adjlist()
                      .groupby('focal')['neighbor']
                      .agg(list).rename('adjacency'))
        if self.id_colname:
            adj_series = adj_series.map(lambda l: [self.gdf.iloc[i][self.id_colname] for i in l])
        return adj_series

    def to_series(self):
        adj_series = self._build_series()
        return pd.concat([self.gdf[self.id_colname], adj_series], axis=1)

    def _build_adjacency(self, gdf):
        from libpysal import weights
        adjacency_mod = getattr(weights, self.adjacency_type)
        return adjacency_mod.from_dataframe(gdf)

    @classmethod
    def from_shapefile(klass, shape_file_path, adjacency_type:str='Queen'):
        import geopandas as gpd
        gdf = gpd.read_file(shape_file_path)
        return klass(gdf, adjacency_type)

    def plot(self):
        import networkx as nx
        # import matplotlib.pyplot as plt

        graph = self.adj.to_networkx()

        # Extract the centroids for connecting the regions, which is
        # the average of the coordinates that define the polygon's boundary
        centroids = np.column_stack((self.gdf.centroid.x, self.gdf.centroid.y))

        # To plot with networkx, we need to merge the nodes back to
        # their positions in order to plot in networkx
        positions = dict(zip(graph.nodes, centroids))

        # plot with a nice basemap
        ax = self.gdf.plot(linewidth=2, edgecolor="grey", facecolor="lightblue")
        nx.draw(graph, positions, ax=ax, node_size=50, node_color="red")

        # plt.show()
        return ax
