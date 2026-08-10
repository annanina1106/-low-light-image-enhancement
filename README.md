# **Multi-modal Low-Light Image Enhancement via Illumination-Structure Fusion**
### **A lightweight, interpretable, and real-time low-light image enhancement system based on Retinex theory.**

## **Introduction**
This project implements a multi-modal image enhancement system specifically targeted at low-light conditions. Adopting a "Divide and Conquer" strategy, we decouple the image into two orthogonal modalities:
  1. **Illumination:** Restored using an enhanced CLAHE pipeline with Region-Aware Masking and Auto-Gamma injection.
  2. **Structure:** Preserved using adaptive bilateral filtering and Sobel operators.

These modalities are recombined using a weighted fusion strategy optimized with de-hazing and gamma recovery curves. The system is capable of handling single images, video files, and real-time webcam streams with YOLOv8 object detection integration.

## **Key Features**
- **Real-time Performance:** Optimized with Vectorized NumPy operations and OpenCV primitives for low-latency video processing.
  https://github.com/user-attachments/assets/e142ca0b-a53c-413f-9a02-9011a4f8738e

- **Interactive GUI:** Fine-tune parameters (Contrast, Detail, Color, Denoise) in real-time.
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/394d3cf9-52fb-4055-ab10-a87e4d636218" />

- **Adaptive Enhancement:** "Auto Mode" automatically detects scene brightness and adjusts Gamma/Denoising parameters.
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/99028f4e-243a-4ecc-b948-c658f28ed58b" />
- **YOLOv8 Integration:** Validates enhancement utility by running object detection on the enhanced stream.
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/f3d953f8-6d35-4bac-b46a-150dc28d971f" />
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/502d6af5-6d5c-4812-a5c8-68b501d2cd59" />

- **Quantitative Evaluation:** Built-in PSNR and SSIM calculation engine for objective benchmarking against Histogram Equalization (HE).
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/3d76aeb4-8cec-47bb-94f9-0da7b2f6473d" />

## **Architecture**

The system pipeline consists of three main stages:
<img width="2942" height="727" alt="image" src="https://github.com/user-attachments/assets/8162bde7-dfee-4ed0-a13e-0695af88955f" />

<img width="2945" height="549" alt="image" src="https://github.com/user-attachments/assets/eb51cb05-d73a-4a90-ae5a-89b20102b0cd" />

**1. Decomposition:** RGB to HSV conversion (processing V-channel).

**2. Modality Processing:** 
  - Illumination: Auto-Gamma -> Region-Aware Masking -> Dual-Path CLAHE.
  - Structure: Adaptive Bilateral Filter -> Sobel Edge Extraction.
**3. Fusion:** Weighted Linear Fusion -> Saturation Boost -> De-hazing -> Gamma Recovery.

## **Installation**

**1. Clone the Repository**

```Bash
   git clone https://github.com/annanina1106/low-light-image-enhancement.git
   cd low-light-image-enhancement
```

**2. Install Dependencies**

Ensure you have Python 3.8+ installed. Install the required libraries:

```Bash
pip install opencv-python numpy matplotlib scikit-image ultralytics pillow
```
(Note: ```tkinter``` is usually included with standard Python installations.)

**3. Prepare YOLO Model (Optional)**

The system will automatically download ```yolov8n.pt``` on the first run of the object detection feature.

## **Usage**

Run the main application:

```Bash
python main.py
```

**GUI Functionality:**

<img width="300" alt="image" src="https://github.com/user-attachments/assets/a1ebc063-7c7d-43be-9916-dbc5d63c66a0" />

- **Button 1 (Interactive GUI):** Adjust parameters manually to visualize the Illumination/Structure decomposition.

- **Button 2 (Single Image Adaptive):** One-click automatic enhancement for static images.

- **Button 3 (Video Enhancement):** Process video files frame-by-frame with de-hazing and brightness recovery.

- **Button 4 (Quantitative Evaluation):** Calculate PSNR/SSIM metrics against a Ground Truth image.

- **Button 5 (YOLO Object Detection Test):** Load a static low-light image to verify object detection performance (Input vs. Enhanced).

- **Button 6 (Webcam Enhancement Only):** Start real-time webcam feed with pure image enhancement (no object detection overlay).

- **Button 7 (Webcam + YOLO):** Run real-time enhancement combined with YOLOv8 object detection.

- **Button 8 (Adaptive vs Fixed Experiment):** Visual comparison to benchmark our "Region-Aware" strategy against standard HE.

## **Project Structure**
```
low-light-image-enhancement/
├── main.py           # Application entry point and GUI logic
├── illumination.py   # Modality A: Brightness enhancement & Masking
├── structure.py      # Modality B: Texture extraction & Denoising
├── fusion.py         # Fusion strategy, De-hazing, & Recovery
├── evaluation.py     # PSNR/SSIM calculation module
├── utils.py          # Helper functions for I/O and visualization
├── README.md         # Project documentation
└── assets/           # Test images & videos (optional)
```
