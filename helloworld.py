# -*- coding: utf-8 -*-
from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

# プロパティのGUIDを取得
property_id = acu.GetBuiltInPropertyId("Zone_ZoneName")

# ゾーン名の値を設定
new_zone_name = act.NormalStringPropertyValue("Hello World!")

# ゾーンを全て取得
zones = acc.GetElementsByType("Zone")

# プロパティ値を入れる配列を作成
property_values = []

# 新しいプロパティ値のリストを作成
for zone in zones:
    property_value = act.ElementPropertyValue(
        zone.elementId, property_id, new_zone_name
    )
    property_values.append(property_value)

# 作成したものをゾーンに適用
acc.SetPropertyValuesOfElements(property_values)