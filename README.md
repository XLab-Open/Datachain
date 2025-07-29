<div align="center">

<img src="./docs/images/ad-multitask.png" width="700" height="160">

<h2 align="center">AI model deployment based on embedded domain controller platforms</h2>


[<span style="font-size:20px;">**Architecture**</span>](./docs/framework.md)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Documentation**</span>](https://liwuhen.cn/CVDeploy-2D)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Blog**</span>](https://www.zhihu.com/column/c_1839603173800697856)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Roadmap**</span>](./docs/roadmap.md)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[<span style="font-size:20px;">**Slack**</span>](https://app.slack.com/client/T07U5CEEXCP/C07UKUA9TCJ)

<p align="right">
  🌐 <b>Language</b> | 语言：
  <a href="./docs/README.zh-CN.md">🇨🇳 中文</a>
</p>

---

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)
![ARM Linux](https://img.shields.io/badge/ARM_Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-%2376B900.svg?style=for-the-badge&logo=nvidia&logoColor=white)
![Performance](https://img.shields.io/badge/Performance-Optimized-red?style=for-the-badge)
![GPU Accelerated](https://img.shields.io/badge/GPU-Accelerated-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

The repository focuses on converting formats across multiple open-source datasets and offers serialization capabilities to unify data representation.
</div>

# Getting Started
Visit our documentation to learn more.
- [Installation](./docs/hpcdoc/source/getting_started/installation.md)
- [Quickstart](./docs/hpcdoc/source/getting_started/Quickstart.md)

# Performances
- Dataset:
    - pascal voc
        > The validation dataset is voc2012.
    - BDD100K
        > The validation dataset is BDD100K, which contains 70000 training samples and 10000 val samples.
    - nuscenes
        > The validation dataset is nuscenes-mini.
- Model: The deployed model is the 's' version of the YOLO multi-task network series.
- Quantize: Quantization was performed using NVIDIA's Post-Training Quantization (PTQ) method.

|Model|Platform|Resolution|mAP50-95(fp32)|mAP50(fp32)|mAP50-95(fp16)|mAP50(fp16)|mAP50-95(int8)|mAP50(int8)|fps(fp32)|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|<a href="https://drive.google.com/drive/folders/1_0YjElSSMCbeTdD2FUbJE6zIHsHhynug" rowspan="3" style="text-align:center; vertical-align:middle; display:flex; justify-content:center; align-items:center; height:100%;">A-YOLOM</a>|RTX4060|480x640|-|-|-|-|-|-|61.8229|
||Orin x|480x640|-|-|-|-|-|-|-|
||Thor|480x640|-|-|-|-|-|-|-|

# ![Contribute](https://img.shields.io/badge/how%20to%20contribute-project-brightgreen) Contributing
Welcome users to participate in these projects. Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for the contributing guideline.We encourage you to join the effort and contribute feedback, ideas, and code. You can participate in Working Groups, Working Groups have most of their discussions on [Slack](https://app.slack.com/client/T07U5CEEXCP/C07UKUA9TCJ).

# ![TODO](https://img.shields.io/badge/how%20to%20contribute-project-brightgreen) TODO
- [ ] Add BDD100K
- [ ] Add API support for Caller

# References
- [Vllm: https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
