# The Steel Manual—in Python!
The goal of this project is to create an open-source Python library to aid in structural steel design following AISC's [*Steel Construction Manual*](https://www.aisc.org/publications/steel-construction-manual-resources/16th-ed-steel-construction-manual/), particularly the [*Specification for Structural Steel Buildings*](https://www.aisc.org/Specification-for-Structural-Steel-Buildings-ANSIAISC-360-22-Download).

Initially, the primary focus will be on limit state checks for non-composite steel members (Chapters D, E, F, G, and H of the *Specification*). The tools developed will be designed both for standalone member checks and for integration with structural analysis packages such as [Pynite](https://pypi.org/project/PyNiteFEA/). Built-in reporting functions powered by [Efficalc](https://pypi.org/project/efficalc/) will aid in design checking and documentation. 

After implementing the limit state checks, I may expand the library to include connection design, composite members, and more.

This is a personal project and is not affiliated with or endorsed by AISC.

## Member Design Progress

|Section Type   |Tension    |Compression   |Flexure    |Shear      |Torsion    |Combined   |
|---------------|-----------|--------------|-----------|-----------|-----------|-----------|
|W, H, and S    |Not started|In progress 🚧|Not started|Not started|Not started|Not started|
|Rectangular HSS|Not started|Not started   |Not started|Not started|Not started|Not started|
|Round HSS      |Not started|Not started   |Not started|Not started|Not started|Not started|
|Pipe           |Not started|Not started   |Not started|Not started|Not started|Not started|
|C and MC       |Not started|Not started   |Not started|Not started|Not started|Not started|
|Single Angles  |Not started|Not started   |Not started|Not started|Not started|Not started|
|Double Angles  |Not started|Not started   |Not started|Not started|Not started|Not started|
|Rectangular Bar|Not started|Not started   |Not started|Not started|Not started|Not started|
|Round Bar      |Not started|Not started   |Not started|Not started|Not started|Not started|
