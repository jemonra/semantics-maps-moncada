# concept-graph-moncada

This project contains the code for the TFG (Trabajo Fin de Grado) "Building and Exploiting Semantic Maps in Robotics Using Large Models", by Jesús Moncada Ramírez, University of Málaga.

## Abstract
Mobile robots are increasingly being deployed in diverse applications across fields such as home assistance, industry, healthcare, or education. A fundamental requirement for these applications, especially when it comes to Human-Robot Interaction (HRI) scenarios, is the robot's ability to interpret and reason about its environment. This ability is often achieved using semantic maps, which enrich the typical geometric/topological representation of the robot workspace with the semantics of its constituent elements (properties, functionalities, relationships, etc.).

Traditional methods for creating these maps rely on object detectors that can only detect those objects previously seen during training, and predefined knowledge bases like ontologies, limiting the robot's adaptability and functionality. This project presents a method for semantic mapping based on large models, including Large Vision-Language Models (LVLMs) and Large Language Models (LLMs), to handle an open set of object categories and dynamic semantic information.

The proposed method, based on ConceptGraphs, utilizes state-of-the-art techniques including Segment Anything (SAM) for object segmentation, CLIP for feature extraction, Gemini 1.5 Pro for generating textual descriptions, and ChatGPT-4o for describing the relationships among objects. The pipeline processes located RGB-D images to create a semantic map represented as a scene graph, where nodes correspond to objects and edges denote their semantic relationships.

The method has been validated using both synthetic (Replica) and real-world (ScanNet) datasets, demonstrating its effectiveness in varied environments. The semantic maps generated are further exploited in an HRI scenario, where an LLM-based chatbot, powered by ChatGPT-4o, assists a mobile robot in helping users perform tasks based on their requests. The use of a self-reflection technique ensures the accuracy and relevance of the robot's actions by refining the LLM's responses. This research improves mobile robot adaptability and intelligence, which is demonstrated by success in controlled and real-world environments.

Keywords: Intelligent Robotics, Semantic maps, Machine learning, Large models.

## Repository contents

All the developed code is written in Python and is contained in the ``src/`` folder. This folder is organized into the following subdirectories:

### ``dataset``
This folder contains utility classes for handling datasets, including:

- Robot@VirtualHome: A dataset on which some tests were carried out.
- ScanNet: A dataset consisting of 3D scans of indoor scenes, used for real-world validation.

### ``llm``
This folder includes classes for generating text using proprietary Large Language Models (LLMs), such as:

- Gemini: Utilized for generating textual descriptions of objects and scenes.
- ChatGPT: Employed for describing relationships among objects and providing contextual understanding in HRI scenarios.

### ``prompt``
This folder contains all the prompts used in the method. These prompts are essential for interacting with the LLMs and guiding their output to generate meaningful semantic information.

### ``slam``
This folder comprises classes related to Simultaneous Localization and Mapping (SLAM) results.

### ``utils``
This folder provides utility classes for various tasks such as:

In the ``data/`` folder some examples of the method execution can be found, especially in the files:
- ``replica_semantic_map.json``: example of a semantic map generated for the ``room0`` sequence from the the Replica dataset.
- ``scannet_semantic_map.json``: example of a semantic map generated for the ``scene0003_02`` sequence from the ScanNet dataset.