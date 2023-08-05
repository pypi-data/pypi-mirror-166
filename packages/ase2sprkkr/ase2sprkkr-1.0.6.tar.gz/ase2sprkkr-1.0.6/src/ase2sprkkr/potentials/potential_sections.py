""" A potential file for SPRKKR is divided to sections. In this module,
there are a generic classes for these sections.
"""

from ..common.configuration_containers import Section
from .io_data import ReadIoData, WriteIoData
from ..sprkkr.sprkkr_atoms import SPRKKRAtoms

class PotentialSection(Section):
    """ A generic class for a section in a potential """

    def _set_from_atoms(self, atoms:SPRKKRAtoms, write_io_data:WriteIoData):
        """ This function should be called before potential file writing to set the propper values to the section.

        Parameters
        ----------
        atoms : SPRKKRAtoms
          Atoms that will be used to create

        write_io_data: WriteIoData
          Object for storing values generated by one section to be (reused in another) - e.g. scaling constants or numbering of meshes etc...
        """
        pass

    def _update_atoms(self, atoms:SPRKKRAtoms, read_io_data:ReadIoData):
        """
        This function should be called after potential file reading to set the values of Atoms object to the ones from the readed file.

        Parameters
        ----------
        atoms : SPRKKRAtoms
          Atoms, whose properties should be set to the values from readed file. Can be None in some sections, then the object will be created
        read_io_data: ReadIoData
          Object for storing values from one section to be used in another one. This mechanism is used to be the sections as independent (and independently testable) as they can be.


        Return
        ------
        atoms: None or SPRKKRAtoms
          If the function creates a new Atoms obejct (either when None has been passed to the atoms args, or when the atoms cannot be adapted to the values readed from the file - e.g. when number of atoms differs) it should return it.
        """
        return None

    def _depends_on(self):
        """ The order of processing of sections during reading can be different than the order during a write. So, if the function should not be processed before given named sections, name then.

        Return
        ------
        prerequisites: [ str, str, ... ]
        """

        return self._definition.depends_on()

    def reset(self):
        self.clear(True)

class UniqueListSection(PotentialSection):
    """ The section, whose data is list of something,
        e.g. of meshes, reference systems etc. The properties
        _value_name and _value_class has to be redefined in the descendants.

        The list of sections object (with numbering of the (unique)
        objects) is stored to io_data during reading/writing to be used
        by the other sections.

        :cvar str _value_name: The name of the property of write_io_data to store the list of data
        :cvar type  _value_class:  The class, that should be created from the list of data

    """

    _value_name : str = None
    """ The name of the property of write_io_data to store the list of data """

    _value_class : type = None
    """ The class, that should be created from the list of data """


    def _set_from_atoms(self, atoms:SPRKKRAtoms, write_io_data: WriteIoData):
        """
        Set the values of the section from the write_io_data.

        :meta public:

        """
        ul = getattr(write_io_data, self._value_name)
        self['DATA'].set([ i.to_tuple() for i in ul.iter_unique()])

    def _update_atoms(self, atoms:SPRKKRAtoms, read_io_data: ReadIoData):
        """
        Update a ReadIoData object accordingly the data in the section:
        set its _value_name to list of self_value_class.from_tuple(<data>)

        :meta public:

        """
        creator = getattr(self._value_class, 'from_tuple', self._value_class)
        read_io_data[self._value_name] = [creator(*i) for i in self['DATA']()]


class ASEArraySection(PotentialSection):
    """ A section, that get and set the given ASE array (see ASE documentation of the
        Atoms class), e.g. magnetization direction.
        The name of the array is given by the section definition in the property array_name
    """

    def has_any_value(self):
        """ Are there data in the section?"""
        return self['DATA'] is not None

    def _depends_on(self):
        """ These sections can be processed after that the Atoms object
            is created.

        :meta public:

        """
        return super()._depends_on() + ['SITES']

    def _set_from_atoms(self, atoms: SPRKKRAtoms, _):
        """
        Just set the values in the section from the Atoms object.
        If the array not exists and the value is mandatory, set it to zero.

        :meta public:
        """
        data = self['DATA']
        try:
          value = atoms.get_array(self._definition.array_name)
        except KeyError:
          if self._definition.is_optional:
             value = None
          else:
             value = data._definition.type.zero_data(len(atoms.positions))
        data.set(value)

    def _update_atoms(self, atoms:SPRKKRAtoms, _):
        """
        Set the array accordingly to the readed data

        :meta public:
        """

        value = self['DATA']()
        atoms.set_array(self._definition.array_name, value)
