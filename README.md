# GHEDesigner - The Flexible and Automatic Ground Heat Exchanger Design Tool

GHEdesigner is a Python package for designing ground heat exchangers (GHE) used with ground source heat pump (GSHP) systems.  Compared to currently available tools such as [GLHEPRO](https://hvac.okstate.edu/glhepro.html), GHEdesigner:
- is flexible. It can synthesize borehole fields that are custom fit to  the user's property description.
- implements the RowWise algorithm (Spitler, et al. 2022)
- is highly automated.  It can select library configurations or custom configurations and determine the final depth requirements.
- has automated conversion of hourly loads to an improved hybrid time step representation, based on the recommendations of Cullin and Spitler (2011).
- is under continuing development at Oklahoma State University (OSU), Oak Ridge National Laboratory (ORNL), and National Renewable Energy Laboratory (NREL).

## Background
GHEdesigner was originally funded through US Department of Energy contract DE‐AC05‐00OR22725 via a subcontract from Oak Ridge National Laboratory.  The first version, called GHEDT, is described in an MS thesis (Cook 2021).   Since that time, the tool has been renamed GHEdesigner, and work has continued at Oklahoma State University, Oak Ridge National Laboratory, and National Renewable Energy Laboratory.

Features added since Cook (2021) include:
- Use of the RowWise algorithm to efficiently place boreholes in the available land area.
- <<<Timothy, Matt: What else?>>>

## Design Algorithms

- This is intended to be an overview of all the design algorithms rather than just the ones that Jack developed.   I plan to cite the relevant papers
- Long time-step g-functions are calculated using pygfunction (Cimmino 2018) using the equivalent borehole method (Prieto and Cimmino 2021).  It's also possible to read g-functions from a library (Spitler, et al. 2021).
- Borehole thermal resistance is computed for single and   double U-tube configurations via the multi-pole method.  For co-axial ground heat exchangers, it is computed from fundamental heat transfer relationships.
- Short time-step g-functions are computed using the Xu and Spitler (2006) method.
- GHEDT contains a novel design methodology for automated selection of borehole fields. The advanced methodology performs optimization based on a target drilling depth. An integer bisection routine is utilized to quickly search over a unimodal domain of boreholes. GHEDT can consider available drilling and no-drilling zones defined as polygons.
- GHEdesigner can synthesize a range of regularly shaped borehole configurations, including previously available shapes (rectangles, open rectangles, L-shape, U-shape, line) and shapes not previously available (C-shapes and zoned rectangles).  More information about these shapes can be found in the documentation for a publicly available g-function library. (Spitler, et al. 2021, 2022b)
- GHEdesigner can synthesize on the fly irregularly shaped borehole configurations using the RowWise algorithm (Spitler, et al. 2022a) or the  bi-uniform polygonal constrained rectangular search (BUPCRS) (Cook 2021).  Both configurations are adapted to the user property boundaries and no-drill zones, if any. Spitler, et al. (2022a) gives an example where the RowWise algorithm saves 12%-18% compared to the BUPCRS algorithm.  The RowWise algorithm takes longer to run, though.
- A set of search routines can be used to size different types of configurations:
- The unconstrained square/near-square search will search a domain of square (n x n) and near-square (n-1 x n) boreholes, with uniform spacing between the boreholes.
- Uniform and bi-uniform constrained rectangular searches will search domains of rectangular configurations that have either uniform spacing or “bi-uniform” spacing – that is, uniform in the x direction and uniform in the y direction, but the two spacings may be different.
- The bi-uniform constrained zoned rectangular search allows for rectangular configurations with different interior and perimeter spacings.
- The bi-uniform polygonal constrained rectangular search (BUPCRS) can search configurations with an outer perimeter and no-go zones described as irregular polygons. This is still referred to as a rectangular search because it is still based on a rectangular grid, from which boreholes that are outside the perimeter or inside a no-go zone are removed.
- The RowWise method generates and searches custom borehole fields that make full use of the available property.  The RowWise algorithms are described by Spitler et al. (2022a).

## Limitations
GHEdesigner does not have every feature that is found in a tool like GLHEPRO.  Features that are currently missing include:
- Heat pumps are not modeled.  Users input heat rejection/extraction rates.
- An hourly simulation is available, but doesn't make use of load aggregation, so is very slow.
- GHEdesigner only covers vertical borehole ground heat exchangers.  Horizontal ground heat exchangers are not treated.
- GHEdesigner does not calculate head loss or warn the user that head loss may be excessive.
- GHEdesigner does not have a graphical user interface.  This limits its usefulness for practicing engineers.
- GHEdesigner is a Python package and requires some Python knowledge to use.  Again, this limits its usefulness for practicing engineers.

## Requirements

GHEDT requires at least Python 3.7 and is tested with Python 3.7 and 3.8. GHEDT  is dependent on the following packages:

- pygfunction (>=2.1)
- numpy (>=1.19.2)
- scipy (>=1.6.2)
- matplotlib (>=3.3.4)
- coolprop (>=6.4.1)
- pandas (>=1.3.2)
- openpyxl (>=3.0.8)
- opencv-python (==4.5.4.58)

## Quick Start

**Users** - Install `ghedt` via the package installer for Python ([pip][#pip]):
```angular2html
pip install ghedt
```

**Developers** - Clone the repository to via git:
```angular2html
git clone https://github.com/j-c-cook/ghedt
```

See [installation](https://github.com/j-c-cook/ghedt/blob/main/INSTALLATION.md)
for more notes on installing. See [ghedt/examples/](https://github.com/j-c-cook/ghedt/tree/main/ghedt/examples)
for usage.

## Questions?

If there are any questions, comments or concerns please [create][#create] an
issue, comment on an [open][#issue] issue, comment on a [closed][#closed] issue,
or [start][#start] a [discussion][#discussion].

## Acknowledgements
The initial release of this work (`ghedt-v0.1`) was financially supported by the U.S. Department of Energy through research subcontracts from Oak Ridge National Laboratory and the National Renewable Energy Laboratory, and by OSU through the Center for Integrated Building Systems, the OG&E Energy Technology Chair, and Oklahoma State University via return of indirect costs to Dr. Jeffrey D. Spitler.

## References
Cimmino, M. 2018. pygfunction: an open-source toolbox for the evaluation of thermal. eSim 2018, Montreál, IBPSA Canada. 492-501.

Cook, J.C. (2021). Development of Computer Programs for Fast Computation of
    g-Functions and Automated Ground Heat Exchanger Design. Master's Thesis,
    Oklahoma State University, Stillwater, OK.

Cullin, J.R. and J.D. Spitler. 2011. A Computationally Efficient Hybrid Time Step
Methodology for Simulation of Ground Heat Exchangers. Geothermics.
40(2): 144-156. https://doi.org/10.1016/j.geothermics.2011.01.001

Prieto, C. and M. Cimmino. 2021. Thermal interactions in large irregular fields of geothermal boreholes: the method of equivalent boreholes. Journal of Building Performance Simulation 14(4): 446-460. https://doi.org/10.1080/19401493.2021.1968953

Spitler, J.D., T.N. West and X. Liu. 2022a. Ground Heat Exchanger Design Tool
with RowWise Placement of Boreholes. IGSHPA Research Track. Las Vegas. Dec. 6-8

Spitler, J. D., T. N. West, X. Liu and I. Borshon 2022b. An open library of g-functions for 34,321 configurations. IGSHPA Research Track. Las Vegas.

Spitler, J. D., J. Cook, T. West and X. Liu 2021. G-Function Library for Modeling Vertical Bore Ground Heat Exchanger, Oak Ridge National Laboratory. https://doi.org/10.15121/1811518

Xu, X. and J. D. Spitler. 2006. _Modelling of Vertical Ground Loop Heat Exchangers with Variable Convective Resistance and Thermal Mass of the Fluid_. 10th International Conference on Thermal Energy Storage - Ecostock 2006, Pomona, NJ. https://hvac.okstate.edu/sites/default/files/pubs/papers/2006/07-Xu_Spitler_06.pdf

[#pygfunction]: https://github.com/MassimoCimmino/pygfunction
[#pip]: https://pip.pypa.io/en/latest/
[#create]: https://github.com/j-c-cook/ghedt/issues/new
[#issue]: https://github.com/j-c-cook/ghedt/issues
[#closed]: https://github.com/j-c-cook/ghedt/issues?q=is%3Aissue+is%3Aclosed
[#start]: https://github.com/j-c-cook/ghedt/discussions/new
[#discussion]: https://github.com/j-c-cook/ghedt/discussions
