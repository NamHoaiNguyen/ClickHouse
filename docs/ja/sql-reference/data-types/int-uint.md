---
slug: /ja/sql-reference/data-types/int-uint
sidebar_position: 2
sidebar_label: UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256
---

# UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256

符号ありまたは符号なしの固定長整数。

テーブルを作成する際、整数に対して数値パラメータを設定することができます（例: `TINYINT(8)`, `SMALLINT(16)`, `INT(32)`, `BIGINT(64)`）が、ClickHouse はこれを無視します。

## Int 範囲

- `Int8` — \[-128 : 127\]
- `Int16` — \[-32768 : 32767\]
- `Int32` — \[-2147483648 : 2147483647\]
- `Int64` — \[-9223372036854775808 : 9223372036854775807\]
- `Int128` — \[-170141183460469231731687303715884105728 : 170141183460469231731687303715884105727\]
- `Int256` — \[-57896044618658097711785492504343953926634992332820282019728792003956564819968 : 57896044618658097711785492504343953926634992332820282019728792003956564819967\]

エイリアス:

- `Int8` — `TINYINT`, `INT1`, `BYTE`, `TINYINT SIGNED`, `INT1 SIGNED`.
- `Int16` — `SMALLINT`, `SMALLINT SIGNED`.
- `Int32` — `INT`, `INTEGER`, `MEDIUMINT`, `MEDIUMINT SIGNED`, `INT SIGNED`, `INTEGER SIGNED`.
- `Int64` — `BIGINT`, `SIGNED`, `BIGINT SIGNED`, `TIME`.

## UInt 範囲

- `UInt8` — \[0 : 255\]
- `UInt16` — \[0 : 65535\]
- `UInt32` — \[0 : 4294967295\]
- `UInt64` — \[0 : 18446744073709551615\]
- `UInt128` — \[0 : 340282366920938463463374607431768211455\]
- `UInt256` — \[0 : 115792089237316195423570985008687907853269984665640564039457584007913129639935\]

エイリアス:

- `UInt8` — `TINYINT UNSIGNED`, `INT1 UNSIGNED`.
- `UInt16` — `SMALLINT UNSIGNED`.
- `UInt32` — `MEDIUMINT UNSIGNED`, `INT UNSIGNED`, `INTEGER UNSIGNED`
- `UInt64` — `UNSIGNED`, `BIGINT UNSIGNED`, `BIT`, `SET`
