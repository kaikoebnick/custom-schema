"""from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from custom_schema.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='NewSchemaPackage',
    description='New schema package entry point configuration.',
    plugin_package='tools',
)"""

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
    MEnum,
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
                    'article doi',
                    'repository',
                    'video',
                    'docker image',
                    'documentation',
                    'hub',
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
        description='Optional field to adding version information.',
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
        description='The short name of the ELN.',
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
                    'fun',
                ]
            ),
        ),
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
