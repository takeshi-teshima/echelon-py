################
Echelon Analysis
################
In this page, we explain the algorithms of echelon analysis using pseudo-code.

********************
1. Echelon Construction
********************

The construction of echelons consist of the following two steps:

#. Peak echelon finding
#. Foundation echelon finding


1.1. Peak Finding Algorithm
====================

#. We repeat the following until we run out of all unsearched indices.

    #. Select one maximum point (summit, :math:`s`) and the max value (summit value, :math:`v`) among the unsearched indices.
       That is, :math:`s \in \mathrm{argmax}_{i \in \mathrm{unsearched}}\mathrm{Data}_i` and :math:`v = \mathrm{Data}_s`.
    #. Initialize :math:`\mathrm{peak}=\{s\}`.
    #. We now run the following extension loop:

        We consider whether to extend :math:`\mathrm{peak}` to newly include
        :math:`S := \mathrm{argmax}_{i \in N} \{\mathrm{Data}_i\}` where :math:`N := \mathrm{nb}(\mathrm{peak})`,
        i.e., the maximizers among the neighbors of :math:`\mathrm{peak}`.
        Here, argmax is understood as a set of indices.

        * If :math:`S` contains no local minimum (i.e., if :math:`\mathrm{Data}_{i} \geq \max_{i \in \mathrm{nb}(N\cup S)}\mathrm{Data}_{i}` where :math:`i \in S`), then we extend the peak set: :math:`\mathrm{peak}\gets \mathrm{peak}\cup S`.
        * Otherwise, we halt the extension loop, flag all elements of :math:`\mathrm{peak}` as searched, register :math:`\mathrm{peak}` as a found peak echelon, and go back to the top of the loop.

#. After the loop is halted, we have the set of found :math:`\mathrm{peak}`'s (which may or may not jointly contain all indices. Those indices that do not belong to a peak echelon will belong to a foundation echelon later.).


1.2. Foundation Finding Algorithm
====================
