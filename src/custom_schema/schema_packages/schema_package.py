"""from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    ) """

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
    description = Quantity(
        type=str,
        description='''You can add text as well as pictures.''',
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity)
    )
    sample_id = Quantity(
        type=str,
        description='''The ID will be automatically generated.''',
    )

    def normalize(self, archive, logger):
        super(Schema, self).normalize(archive, logger)

        if self.sample_id is None:
            self.sample_id = f'{self.date_and_time}--{self.measurement_name}'


m_package.__init_metainfo__()
