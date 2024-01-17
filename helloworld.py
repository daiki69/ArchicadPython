# -*- coding: utf-8 -*-
from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

# �v���p�e�B��GUID���擾
property_id = acu.GetBuiltInPropertyId("Zone_ZoneName")

# �]�[�����̒l��ݒ�
new_zone_name = act.NormalStringPropertyValue("Hello World!")

# �]�[����S�Ď擾
zones = acc.GetElementsByType("Zone")

# �v���p�e�B�l������z����쐬
property_values = []

# �V�����v���p�e�B�l�̃��X�g���쐬
for zone in zones:
    property_value = act.ElementPropertyValue(
        zone.elementId, property_id, new_zone_name
    )
    property_values.append(property_value)

# �쐬�������̂��]�[���ɓK�p
acc.SetPropertyValuesOfElements(property_values)