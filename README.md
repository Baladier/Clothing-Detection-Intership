# ROS Clothing Detection

A **ROS Noetic** package that detects clothing items in a live video stream and
publishes each detection as a bounding box with its class label and confidence
score. It runs **YOLOv3 trained on ModaNet**, executed through the
[ailia](https://github.com/axinc-ai/ailia-models/tree/master/deep_fashion/clothing-detection)
runtime.

Recognises 13 classes: `bag`, `belt`, `boots`, `footwear`, `outer`, `dress`,
`sunglasses`, `pants`, `top`, `shorts`, `skirt`, `headwear`, `scarf/tie`.

<!-- TODO: replace with a real screenshot or GIF of the system running.
![Demo](docs/demo.gif)
-->

> **Project status.** The two nodes in `src/` are functional and together form a
> complete clothing-detection pipeline. An additional person re-identification
> module was left unfinished; its code is kept in [`wip/`](wip/) for reference
> but is **not runnable**. See [wip/README.md](wip/README.md) for details.

---

## Architecture

```
┌──────────────────┐   /image_output    ┌────────────────────────────┐
│  camera_node.py  │ ─────────────────► │ clothing_detector_node.py  │
│  webcam capture  │  sensor_msgs/Image │ YOLOv3-ModaNet (ailia)     │
└──────────────────┘                    └────────────────────────────┘
                                                     │
                                                     │ /clothing_detector/results
                                                     ▼   clothing_detection/BoxArray
                                          ┌────────────────────────┐
                                          │    any consumer node   │
                                          └────────────────────────┘
```

### Topics

| Node | Direction | Topic | Message |
|---|---|---|---|
| `camera_node` | publishes | `/image_output` | `sensor_msgs/Image` |
| `clothing_detector_node` | subscribes | `/image_output` | `sensor_msgs/Image` |
| `clothing_detector_node` | publishes | `/clothing_detector/results` | `clothing_detection/BoxArray` |

### Messages

`Box.msg` describes a single garment; `BoxArray.msg` groups all garments found
in one frame.

```
# Box.msg
string  class_id   # garment label
float32 prob       # confidence in [0, 1]
int32   x          # top-left corner
int32   y
int32   width
int32   height
```

---

## Requirements

- Ubuntu 20.04 with **ROS Noetic**
- Python 3.8
- A webcam or USB camera
- The ailia runtime requires a licence; see the
  [ailia-models repository](https://github.com/axinc-ai/ailia-models)

---

## Installation

```bash
# 1. Catkin workspace
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone https://github.com/Baladier/Deteccion-de-ropa.git clothing_detection

# 2. Python environment
conda create -n clothing_det_env python=3.8
conda activate clothing_det_env
pip install -r clothing_detection/requirements.txt

# 3. Build
cd ~/catkin_ws
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3
source devel/setup.bash
```

The cloned directory must be named `clothing_detection` inside `src/` — that is
the ROS package name, and message imports resolve against it.

Model weights (`.onnx` and `.prototxt`) are downloaded automatically the first
time the detector starts and are stored in `models/`.

---

## Usage

Single command:

```bash
roslaunch clothing_detection clothing_detection.launch
```

Or node by node, each in its own terminal:

```bash
roscore
rosrun clothing_detection camera_node.py
rosrun clothing_detection clothing_detector_node.py
```

To inspect detections:

```bash
rostopic echo /clothing_detector/results
```

### Parameters

| Parameter | Node | Default | Description |
|---|---|---|---|
| `~camera_index` | `camera_node` | `0` | Video device opened by OpenCV. |
| `~image_topic` | both | `/image_output` | Topic linking camera and detector. |
| `~fps` | `camera_node` | `10` | Publishing rate. |
| `~threshold` | `clothing_detector_node` | `0.15` | Minimum detection confidence. |
| `~iou` | `clothing_detector_node` | `0.4` | IoU threshold for non-maximum suppression. |
| `~detection_width` | `clothing_detector_node` | `640` | Model input resolution. |

Example:

```bash
roslaunch clothing_detection clothing_detection.launch threshold:=0.30 camera_index:=2
```

---

## Repository layout

```
.
├── src/
│   ├── camera_node.py              # Publishes webcam frames
│   └── clothing_detector_node.py   # Clothing detection (YOLOv3-ModaNet)
├── msg/
│   ├── Box.msg
│   └── BoxArray.msg
├── launch/
│   └── clothing_detection.launch
├── wip/                            # Unfinished module, not runnable
│   ├── visualization.py
│   └── README.md
├── models/                         # Weights, downloaded on first run (git-ignored)
├── CMakeLists.txt
├── package.xml
└── requirements.txt
```

---

## Known limitations

- The detector processes the full frame rather than per-person regions of
  interest, so with multiple people in view garments are not attributed to a
  specific individual.
- Single-camera setup only.
- No temporal tracking: each frame is processed independently.

---

## Credits

Clothing detection model: [axinc-ai/ailia-models](https://github.com/axinc-ai/ailia-models/tree/master/deep_fashion/clothing-detection),
YOLOv3 trained on the ModaNet dataset.

## Licence

MIT — see [LICENSE](LICENSE).

## Author

**Alan Beltrán** — Mechatronics Engineer, UDLAP
[GitHub](https://github.com/Baladier) <!-- TODO: add LinkedIn -->
