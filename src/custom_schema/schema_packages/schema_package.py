"""from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    ) 

from nomad.config import config
from nomad.datamodel.data import (
Datetime,
Schema,
)
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import MEnum, Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    'custom_schema.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class NewSchemaPackage(Schema):
    measurement_name = Quantity(
        type=str, 
        description='''A nice and short name for your measurement.''',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity)
    )
    date_and_time = Quantity(
        type=Datetime,
        description='''Date and time the measurement was taken.''',
        #default=
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateTimeEditQuantity)
    )
    material = Quantity(
        type=str, 
        description='''Enter your material.''',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            suggestions=['gold', 'silver'],
        )
    )
    nice_peak = Quantity(
        type=bool,
        description='''Check if there is a nice peak in the measurement.''',
        a_eln=ELNAnnotation(component=ELNComponentEnum.BoolEditQuantity) #default
    )
    measurement_category = Quantity(
        type=MEnum('calibration', 'real_measurment'),
        description='''Choose your category.''',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.RadioEnumEditQuantity,
        )
    )
    voltage = Quantity(
        type=float,
        description='''Enter your voltage.''',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        )
    )
    number_of_people_killed_during_measurement = Quantity(
        type=int,
        description='''Let us hope it is a zero.''',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.SliderEditQuantity,
            minValue=0,
            maxValue=50,
        )
    )
    description = Quantity(
        type=str,
        description='''You can add text as well as pictures.''',
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity)
    )
    sample_id = Quantity(
        type=str,
        description='''The ID will be automatically generated.''',
        a_eln=ELNAnnotation(default=f'{date_and_time}--{measurement_name}'),
    )


m_package.__init_metainfo__()"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

import xml

from nomad.datamodel.data import (
    ArchiveSection,
    EntryDataCategory,
    Schema,
)
from nomad.datamodel.data import Author as NomadAuthor
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import (
    Category,
    Datetime,
    #MEnum,
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)

m_package = SchemaPackage(name='laserphysics ELN schema')


class ToolsCategory(EntryDataCategory):
    m_def = Category(label='Basic ELN', categories=[EntryDataCategory])


def remove_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())


class Material(ArchiveSection):
    m_def = Section(a_eln=ELNAnnotation(overview=True))

    name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Name of the material.',
    )
    formula = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Chemical formula of the material.',
    )


"""class System(ArchiveSection):
    m_def = Section(a_eln=ELNAnnotation(overview=True))

    name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Specifying name of the system.',
    )"""


class Author(ArchiveSection):
    m_def = Section(a_eln=ELNAnnotation(overview=True))

    first_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity, label='First Name'
        ),
        description='First name of the author',
    )

    last_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity, label='Last Name'
        ),
        description='Last name of the author.',
    )


class Reference(ArchiveSection):
    m_def = Section(a_eln=ELNAnnotation(overview=True))

    kind = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            props=dict(
                suggestions=[
                    'article url',
                    'dataset url',
                    'video url',
                    'picture url',
                    'documentation',
                    'other',
                ]
            ),
        ),
    )

    name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Human readable name for the reference.',
    )

    description = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity),
        description='Extra details about the reference.',
    )

    uri = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.URLEditQuantity, label='URI'),
        description='External URI for the reference.',
    )

    version = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Optional field for adding version information.',
    )


class laserphysicsELN(Schema):
    m_def = Section(
        label='laserphysics ELN schema',
        categories=[ToolsCategory],
        a_eln=ELNAnnotation(),
    )

    name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        label='Name/Title',
        description='Short name of the ELN.',
    )

    date = Quantity(
        type=Datetime,
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity),
        label='Last update',
        description='The date of the last update.',
    )

    description = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity),
        description='Short description of the ELN. You can add pictures!',
    )

    category = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            props=dict(
                suggestions=[
                    'measurement',
                    'calibration',
                    'other',
                ]
            ),
        ),
    )

    tag_1 = Quantity(
        type=bool,
        description='''Check if there is a nice peak in tag_1.''',
        a_eln=ELNAnnotation(component=ELNComponentEnum.BoolEditQuantity)
    )

    voltage = Quantity(
        type=float,
        description='''Enter your voltage.''',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        )
    )
    number_of_people_killed_during_measurement = Quantity(
        type=int,
        description='''Let us hope it is zero.''',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.SliderEditQuantity,
            minValue=0,
            maxValue=50,
        )
    )

    """platform = Quantity(
        type=MEnum(['Python', 'Julia', 'R', 'other']),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.AutocompleteEditQuantity,
        ),
    )"""

    authors = SubSection(section=Author, repeats=True)

    material = SubSection(section=Material, repeats=True)

#    systems = SubSection(section=System, repeats=True)

    references = SubSection(section=Reference, repeats=True)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        if self.name:
            archive.metadata.entry_name = self.name

        if self.description:
            if self.description.startswith('<'):
                comment = remove_tags(self.description)
            else:
                comment = self.description

            archive.metadata.comment = comment

        if self.authors:
            archive.metadata.entry_coauthors = [
                NomadAuthor(**author.m_to_dict()) for author in self.authors
            ]


m_package.__init_metainfo__()
