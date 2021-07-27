---
Name: "Guff"
STR: (1d6+6)*5
CON: (2d6+6)*5
SIZ: (3d6+6)*5
DEX: (4d6+6)*5
INT: (5d6+6)*5
POW: (6d6+6)*5
HitPoints: ($CON + $SIZ) // 10
MagicPoints: $POW // 5
Move: if $DEX < $SIZ and $STR < $SIZ then 7 elif $STR > $SIZ and $DEX > $SIZ then 9 else 8
---
# {{ Name }}

## Origin

From the mind of the developer

## Stats

|     |           |
|-----|-----------|
| STR | {{ STR }} |
| CON | {{ CON }} |
| SIZ | {{ SIZ }} |
| DEX | {{ DEX }} |
| INT | {{ INT }} |
| POW | {{ POW }} |

Hitpoints: {{ HitPoints }}
Magic points: {{ MagicPoints }}
Move: {{ Move }}
