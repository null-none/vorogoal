# vorogoal

vorogoal is a lightweight Python library for visualizing spatial control in football using Voronoi diagrams.

### Example

```python
from vorogoal.pitch_voronoi import PitchVoronoi

team1 = [[10, 10], [20, 20], [30, 20]]
team2 = [[15, 15], [25, 25], [25, 35]]

voro = PitchVoronoi(pitch_image_path="pitch.png")
voro.set_players(team1, team2, team1_color="red", team2_color="blue")
voro.draw()
```


### License

MIT
