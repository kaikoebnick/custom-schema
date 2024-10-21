from nomad.config.models.plugins import SchemaPackageEntryPoint


class custom_schemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from custom_schema.schema_packages import m_package

        return m_package


custom_schema = custom_schemaPackageEntryPoint(
    name='Laserphysics ELN',
    description='Describes the basic schemas for laserphysics notebooks.',
)
