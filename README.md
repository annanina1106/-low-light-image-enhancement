# **Multi-modal Low-Light Image Enhancement via Illumination-Structure Fusion**
### **A lightweight, interpretable, and real-time low-light image enhancement system based on Retinex theory.**
- **Course:** Multi-Modality Image Processing, MMIP Final Project
- **Institution:** National Yang Ming Chiao Tung University (NYCU)
- **Authors:** Wei-Chen Wang, Na Li, Wei-Shiue Hung

## **📖 Introduction**
This project implements a multi-modal image enhancement system specifically targeted at low-light conditions. Adopting a "Divide and Conquer" strategy, we decouple the image into two orthogonal modalities:
  1. **Illumination:** Restored using an enhanced CLAHE pipeline with Region-Aware Masking and Auto-Gamma injection.
  2. **Structure:** Preserved using adaptive bilateral filtering and Sobel operators.
     
These modalities are recombined using a weighted fusion strategy optimized with de-hazing and gamma recovery curves. The system is capable of handling single images, video files, and real-time webcam streams with YOLOv8 object detection integration.

## **🚀 Key Features**
- **⚡ Real-time Performance:** Optimized with Vectorized NumPy operations and OpenCV primitives for low-latency video processing.
- **🎛️ Interactive GUI:** Fine-tune parameters (Contrast, Detail, Color, Denoise) in real-time.
- **🧠 Adaptive Enhancement:** "Auto Mode" automatically detects scene brightness and adjusts Gamma/Denoising parameters.
- **👁️ YOLOv8 Integration:** Validates enhancement utility by running object detection on the enhanced stream.
- **📊 Quantitative Evaluation:** Built-in PSNR and SSIM calculation engine for objective benchmarking against Histogram Equalization (HE).

## **🛠️ Architecture**

The system pipeline consists of three main stages:

**1. Decomposition:** RGB to HSV conversion (processing V-channel).

**2. Modality Processing:** 
  - Illumination: Auto-Gamma -> Region-Aware Masking -> Dual-Path CLAHE.
  - Structure: Adaptive Bilateral Filter -> Sobel Edge Extraction.
**3. Fusion:** Weighted Linear Fusion -> Saturation Boost -> De-hazing -> Gamma Recovery.

## **💻 Installation**

**1. Clone the Repository**

```Bash
   git clone https://github.com/neve1008/low-light-image-enhancement.git
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

## **🎮 Usage**

Run the main application:

```Bash
python main.py
```

**GUI Functionality:**

- **Button 1 (Interactive GUI):** Adjust parameters manually to visualize the Illumination/Structure decomposition.

- **Button 2 (Single Image Adaptive):** One-click automatic enhancement for static images.

- **Button 3 (Video Enhancement):** Process video files frame-by-frame with de-hazing and brightness recovery.

- **Button 4 (Quantitative Evaluation):** Calculate PSNR/SSIM metrics against a Ground Truth image.

- **Button 5 (YOLO Object Detection Test):** Load a static low-light image to verify object detection performance (Input vs. Enhanced).

- **Button 6 (Webcam Enhancement Only):** Start real-time webcam feed with pure image enhancement (no object detection overlay).

- **Button 7 (Webcam + YOLO):** Run real-time enhancement combined with YOLOv8 object detection.

- **Button 8 (Adaptive vs Fixed Experiment):** Visual comparison to benchmark our "Region-Aware" strategy against standard HE.

## **📂 Project Structure**
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

## **👥 Contributors**

- **Wei-Chen Wang**
- **Na Li**
- **Wei-Shiue Hung**

College of Artificial Intelligence, National Yang Ming Chiao Tung University.
