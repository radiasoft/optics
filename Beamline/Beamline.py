"""
Represents a beamline.

BeamlineComponents can be attached at positions(BeamlinePosition), i.e. longitudinal, off-axis and inclined.
We can iterate of the components, find their positions or look for a specific component.
"""

class Beamline(object):
    def __init__(self):
        self._components = []
        self._positions = []

    def _findComponentInsertionIndex(self, beamline_position):
        insert_index = 0

        for position in self._positions:
            if position.z()>beamline_position.z():
                break

            insert_index += 1

        return insert_index

    def attachComponentAt(self, beamline_component, beamline_position):

        insert_index = self._findComponentInsertionIndex(beamline_position)

        self._components.insert(insert_index,beamline_component)
        self._positions.insert(insert_index,beamline_position)

    def positionOf(self, beamline_component):
        component_index = self._components.index(beamline_component)
        position = self._positions[component_index]

        return position

    def componentByIndex(self, index):
        if index < len(self._components):
            return self._components[index]

        return None

    def componentByName(self, component_name):
        for component in self._components:
            if component.name() == component_name:
                return component

        return None

    def __iter__(self):
        self._iter_component_index = 0
        return self

    def __next__(self):
        if self._iter_component_index>=len(self._components):
            raise StopIteration

        component = self._components[self._iter_component_index]
        self._iter_component_index+=1
        return component