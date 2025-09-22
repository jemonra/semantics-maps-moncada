# semantics-maps-moncada

Code for the B.Sc. Final Thesis: "Building and Exploiting Semantic Maps in Robotics Using Large Models".
- Author: [Jesús Moncada Ramírez](https://github.com/jemonra), University of Málaga, academic year 2023-2024.

![Semantic mapping method overview](docs/english_overview.png "Local Image")

## 1. Overview

Mobile robots benefit from semantic maps that augment geometry and topology with object properties, functions, and relationships—crucial in HRI scenarios. Traditional pipelines rely on closed‑set detectors and fixed ontologies. This project adopts Large Vision–Language Models (LVLMs) and Large Language Models (LLMs) to support an open set of categories and dynamic semantics.

Built on [ConceptGraphs](https://concept-graphs.github.io/), the pipeline uses:
- Segment Anything (SAM) for object segmentation
- CLIP for feature extraction
- Gemini 1.5 Pro for textual descriptions
- ChatGPT-4o for relationship inference

RGB‑D inputs are converted into a scene graph where nodes are objects and edges are semantic relations. Validation spans synthetic (Replica) and real‑world (ScanNet) datasets. The maps are further exploited in an HRI setting through an LLM‑based chatbot with self‑reflection to refine answers.

This work resulted in a paper presented at the conference Jornadas de Automática 2024 (Málaga, Spain) titled [_"Modelos a gran escala para mapeo semántico en robótica móvil"_](https://revistas.udc.es/index.php/JA_CEA/article/view/10940) (_Large models for semantic mapping in mobile robotics_).

## 2. Repository Contents

The code contained in this repository is organized into these main folders:

### `concept-graphs/`

Since our work is based on [ConceptGraphs](https://concept-graphs.github.io/) and we needed to apply some modifications to the original code to make it work in our context, we provide here the original ConcepGraphs code with these modifications.


The project is organized into these main folders:

### `src/`
Holds all Python source code, structured in several subfolders:

- `dataset/` – Dataset utilities and loaders.
  - `Robot@VirtualHome`: used for experimental tests.
  - `ScanNet`: real 3D indoor scans for validation.
- `llm/` – Interfaces for Large Language Models.
  - `Gemini`: creates textual descriptions of objects and scenes.
  - `ChatGPT`: infers object relationships and provides context for HRI.
- `prompt/` – Prompt files used to query the LLMs and guide their output.
- `slam/` – Classes and functions for handling Simultaneous Localization and Mapping (SLAM) results.
- `utils/` – General utilities such as data handling helpers, geometry tools, and I/O functions.

### `data/`
Contains sample outputs of the method:
- `replica_semantic_map.json` – Semantic map generated for the `room0` sequence of the Replica dataset.
- `scannet_semantic_map.json` – Semantic map generated for the `scene0003_02` sequence of the ScanNet dataset.

### `scripts/`
Executable scripts to run the full pipeline on different datasets.  
Before using them, install the required libraries and datasets following the
[ConceptGraphs instructions](https://github.com/concept-graphs/concept-graphs).  
You can skip the LLaVA installation, as this project replaces it with `Gemini` and `ChatGPT`.

Script name prefixes indicate the dataset and phase:
- `cg*`, `cgf*`, `replica*` – Run processes on Replica sequences.
- `ravh*` – Run processes on Robot@VirtualHome (experimental, not all phases implemented).
- `sn*` – Run processes on ScanNet sequences.

## 3. Documentation

For a detailed explanation of the semantic mapping method developed and the exploitation of the generated semantic maps, refer to:
- [Final Thesis Report](docs/Memoria.pdf)
- [Final Presentation Slides](docs/Presentacion.pdf)