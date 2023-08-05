<div align="center">
<h1>
DetHub: Object Detection Model Hub
</h1>
<img src="https://raw.githubusercontent.com/goksenin-uav/torchreid-pip/main/doc/torchvision.jpg" alt="Torchvision" width="800">
</div>

### Installation
```
pip install dethub
```
### Yolov5 Object Prediction and Visualization
```python
from dethub.model import Yolov5
from dethub.visualize import show

detection_model = Yolov5(model_path= "yolov5s.pt", device="cpu", confidence_threshold=0.5, image_size=640)
show("highway1.jpg", detection_model)
```
<img src="https://raw.githubusercontent.com/goksenin-uav/torchreid-pip/main/doc/yolov5.jpg" alt="Yolov5" width="800">

### Torchvision Object Prediction and Visualization
```python
from dethub.model import TorchVision
from dethub.visualize import show

detection_model = TorchVision(model_path= "dethub/models/torchvision/fasterrcnn_resnet50_fpn.pth", device="cpu", confidence_threshold=0.5, image_size=640)
show("highway1.jpg", detection_model)
```
<img src="https://raw.githubusercontent.com/goksenin-uav/torchreid-pip/main/doc/torchvision.jpg" alt="Torchvision" width="800">

### TensorflowHub Object Prediction and Visualization
```python
from dethub.model import TensorflowHub
from dethub.visualize import show

detection_model = TensorflowHub(model_path= "https://tfhub.dev/tensorflow/efficientdet/d3/1", device="cpu", confidence_threshold=0.5, image_size=640)
show("highway1.jpg", detection_model)
```
<img src="https://raw.githubusercontent.com/goksenin-uav/torchreid-pip/main/doc/tensorflow.jpg" alt="TfHub" width="800">

### Contributing
Before opening a PR:
- Reformat with black and isort:
```bash
black . --config pyproject.toml
isort .
```
References:
- [SAHI](https://github.com/obss/sahi)
- [YOLOX](https://github.com/Megvii-BaseDetection/YOLOX)
- [Mcvarer](https://github.com/mcvarer/coco_toolkit)
