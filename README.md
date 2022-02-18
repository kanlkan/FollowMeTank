# FollowMeTank
Application for caterpillar tank with Nvidia Jetson Nano which follows me.

# Environment
* Development on Jetson Nano(Linux Jetson-nano 4.9.140-tegra aarch64 GNU/Linux)
    * python:3.6.9
    * OpenCV:4.5.2 (built with face, dnn library)
# Materials
* Jetson Nano
    * https://www.nvidia.com/ja-jp/autonomous-machines/embedded-systems/jetson-nano/

* CSI Camera for Jetson Nano
    * https://www.amazon.co.jp/Jetson-Nano-IMX219-160-%E8%A7%A3%E5%83%8F%E5%BA%A6160%E5%BA%A6%E5%BA%83%E8%A7%92-IMX219%E3%82%BB%E3%83%B3%E3%82%B5%E3%83%BC%E4%BB%98%E3%81%8D/dp/B07T43K7LC

* Caterpillar kit
    * https://www.tamiya.com/japan/products/70170/index.html

* Mobile Battery (Output:5V/3A and 5V/2.4A)
    * https://www.elecom.co.jp/products/DE-C18L-10000WF.html

* Regulator PQ3RD23(3.3V/2A)
    * https://akizukidenshi.com/catalog/g/gI-01177/

* Motor Driver DRV8835
    * https://akizukidenshi.com/catalog/g/gK-09848/

* Some others electronics parts
    * Condensers, Jamper wires, etc

# Wiring
![Wiring Jetson Nano J41 and ICs](https://github.com/kanlkan/FollowMeTank/blob/main/resource/Wiring_JetsonNano_ICs.png)

# AI/ComputerVision
* Face Detector
    * Object Detection with ResNet10
        * Face Detector model : https://github.com/sr6033/face-detection-with-OpenCV-and-DNN

* Face Recognizer
    * Fisher Face
        * https://docs.opencv.org/4.5.2/d2/de9/classcv_1_1face_1_1FisherFaceRecognizer.html
# Pictures
![FolloMe Tank](https://github.com/kanlkan/FollowMeTank/blob/main/resource/caterpillar.JPG)
![Example for moving tank](https://github.com/kanlkan/FollowMeTank/blob/main/resource/follow_me_tank.gif)

# Detail resorce (in Japanese)
https://qiita.com/kanlkan/items/e18a075f1060559b8d7b
