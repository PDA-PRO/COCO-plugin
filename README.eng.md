# COCO-plugin

[한국어](https://github.com/PDA-PRO/COCO-plugin/blob/main/README.md)|English  
Easily apply various extension functions using AI, such as AI problem generation and AI answer generation, through plugins.
If you want to develop a new plugin, please refer to https://github.com/PDA-PRO/COCO-plugin/blob/main/README.develop.md

## List of plugins that can be added to COCO

- [AI answer generation](https://github.com/PDA-PRO/COCO-plugin/tree/main/answer_generation)
- [code cluster](https://github.com/PDA-PRO/COCO-plugin/tree/main/code_cluster)
- [AI code improvements](https://github.com/PDA-PRO/COCO-plugin/tree/main/code_improvement)
- [AI problem creation](https://github.com/PDA-PRO/COCO-plugin/tree/main/problem_generation)
- [Wong Part of Code](https://github.com/PDA-PRO/COCO-plugin/tree/main/wpc)
  **Additional settings are required for application. Please visit the link and make additional settings**

## precondition

### COCO Installation

Install by referring to https://github.com/PDA-PRO/COCO-deploy  
By default, the `plugin` folder exists in the path where `docker up` was executed.

## Apply plugin

### Linux

- System: Ubuntu 20.04.6 LTS

#### Download plugin list

```bash
git clone https://github.com/PDA-PRO/COCO-plugin.git
cd COCO-plugin
```

#### Move the desired plugin folder to the `plugin` folder

```bash
cp <Plugin folder> <plugin folder path>/<Plugin folder>
```

#### Restart coco_backend container

```bash
docker container restart coco_backend
```

### Windows

- System: Windows 10

#### Download plugin list

```bash
git clone https://github.com/PDA-PRO/COCO-plugin.git
cd COCO-plugin
```

#### Move the desired plugin folder to the `plugin` folder

#### Restart coco_backend container

```bash
docker container restart coco_backend
```

## Use

#### AI PLUGINS menu on administrator page

![manage](https://github.com/PDA-PRO/COCO-plugin/assets/80380576/cc8fcf7a-d4c8-4152-a206-107817fcf003)

- You can check the status of the backend and frontend of the applied plugin
- Plug-in endpoint on/off possible
