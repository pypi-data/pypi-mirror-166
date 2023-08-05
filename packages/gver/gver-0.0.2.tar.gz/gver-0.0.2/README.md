# GVer

Install from [PyPI](https://pypi.org/project/gver/):

```
pip install gver
```

https://user-images.githubusercontent.com/57521167/188253395-374dde18-8ce5-42c0-8f70-4d075bbb6ba7.mp4


```python
from manim import *
from gver import GVer

class Demo(Scene):
    def construct(self):
        dot = Dot().to_corner(UL)
        gver = GVer()

        self.add(gver, dot)
        self.wait()

        gver.add_updater(lambda m: m.watch(dot))
        self.play(dot.animate(run_time=3).to_corner(UR))
        gver.clear_updaters()

        gver.stop_watch()
        gver.wink(self, 2)
        self.wait()

        gver.close_eye(left=True)
        self.wait()
```
