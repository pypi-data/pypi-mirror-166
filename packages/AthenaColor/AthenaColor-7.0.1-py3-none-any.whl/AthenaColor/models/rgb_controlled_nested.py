# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

from typing import Any
# Custom Library

# Custom Packages
from AthenaColor.func.ansi_sequences import color_sequence_nested
from AthenaColor.func.ansi_sequences import color_sequence
from AthenaColor.models.rgb_controlled import RgbControlled
import AthenaColor.data.colors_html as HtmlColorObjects

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
sep_=" "

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class RgbControlledNested:
    _inline_class:RgbControlled
    _reset:str

    def __init__(self, inline_class:RgbControlled, reset:str):
        self._inline_class = inline_class
        self._reset = reset

    def custom(self,*obj:tuple[Any, ...], color:tuple[int,int,int], sep:str=sep_) -> str:
        return color_sequence_nested(
            obj,
            color_sequence(f"{self._inline_class.param_code}{color[0]};{color[1]};{color[2]}"),
            self._reset,
            sep=sep
        )

    # ------------------------------------------------------------------------------------------------------------------
    def Maroon(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MAROON,sep=sep)

    def DarkRed(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKRED,sep=sep)

    def Brown(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BROWN,sep=sep)

    def Firebrick(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.FIREBRICK,sep=sep)

    def Crimson(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CRIMSON,sep=sep)

    def Red(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.RED,sep=sep)

    def Tomato(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.TOMATO,sep=sep)

    def Coral(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CORAL,sep=sep)

    def IndianRed(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.INDIANRED,sep=sep)

    def LightCoral(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTCORAL,sep=sep)

    def DarkSalmon(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKSALMON,sep=sep)

    def Salmon(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SALMON,sep=sep)

    def LightSalmon(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTSALMON,sep=sep)

    def OrangeRed(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ORANGERED,sep=sep)

    def DarkOrange(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKORANGE,sep=sep)

    def Orange(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ORANGE,sep=sep)

    def Gold(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GOLD,sep=sep)

    def DarkGoldenRod(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKGOLDENROD,sep=sep)

    def GoldenRod(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GOLDENROD,sep=sep)

    def PaleGoldenRod(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PALEGOLDENROD,sep=sep)

    def DarkKhaki(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKKHAKI,sep=sep)

    def Khaki(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.KHAKI,sep=sep)

    def Olive(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.OLIVE,sep=sep)

    def Yellow(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.YELLOW,sep=sep)

    def YellowGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.YELLOWGREEN,sep=sep)

    def DarkOliveGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKOLIVEGREEN,sep=sep)

    def OliveDrab(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.OLIVEDRAB,sep=sep)

    def LawnGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LAWNGREEN,sep=sep)

    def Chartreuse(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CHARTREUSE,sep=sep)

    def GreenYellow(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GREENYELLOW,sep=sep)

    def DarkGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKGREEN,sep=sep)

    def Green(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GREEN,sep=sep)

    def ForestGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.FORESTGREEN,sep=sep)

    def Lime(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIME,sep=sep)

    def LimeGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIMEGREEN,sep=sep)

    def LightGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTGREEN,sep=sep)

    def PaleGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PALEGREEN,sep=sep)

    def DarkSeaGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKSEAGREEN,sep=sep)

    def MediumSpringGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMSPRINGGREEN,sep=sep)

    def SpringGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SPRINGGREEN,sep=sep)

    def SeaGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SEAGREEN,sep=sep)

    def MediumAquaMarine(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMAQUAMARINE,sep=sep)

    def MediumSeaGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMSEAGREEN,sep=sep)

    def LightSeaGreen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTSEAGREEN,sep=sep)

    def DarkSlateGray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKSLATEGRAY,sep=sep)

    def Teal(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.TEAL,sep=sep)

    def DarkCyan(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKCYAN,sep=sep)

    def Aqua(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.AQUA,sep=sep)

    def Cyan(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CYAN,sep=sep)

    def LightCyan(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTCYAN,sep=sep)

    def DarkTurquoise(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKTURQUOISE,sep=sep)

    def Turquoise(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.TURQUOISE,sep=sep)

    def MediumTurquoise(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMTURQUOISE,sep=sep)

    def PaleTurquoise(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PALETURQUOISE,sep=sep)

    def AquaMarine(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.AQUAMARINE,sep=sep)

    def PowderBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.POWDERBLUE,sep=sep)

    def CadetBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CADETBLUE,sep=sep)

    def SteelBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.STEELBLUE,sep=sep)

    def CornFlowerBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CORNFLOWERBLUE,sep=sep)

    def DeepSkyBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DEEPSKYBLUE,sep=sep)

    def DodgerBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DODGERBLUE,sep=sep)

    def LightBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTBLUE,sep=sep)

    def SkyBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SKYBLUE,sep=sep)

    def LightSkyBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTSKYBLUE,sep=sep)

    def MidnightBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MIDNIGHTBLUE,sep=sep)

    def Navy(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.NAVY,sep=sep)

    def DarkBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKBLUE,sep=sep)

    def MediumBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMBLUE,sep=sep)

    def Blue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BLUE,sep=sep)

    def RoyalBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ROYALBLUE,sep=sep)

    def BlueViolet(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BLUEVIOLET,sep=sep)

    def Indigo(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.INDIGO,sep=sep)

    def DarkSlateBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKSLATEBLUE,sep=sep)

    def SlateBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SLATEBLUE,sep=sep)

    def MediumSlateBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMSLATEBLUE,sep=sep)

    def MediumPurple(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMPURPLE,sep=sep)

    def DarkMagenta(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKMAGENTA,sep=sep)

    def DarkViolet(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKVIOLET,sep=sep)

    def DarkOrchid(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKORCHID,sep=sep)

    def MediumOrchid(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMORCHID,sep=sep)

    def Purple(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PURPLE,sep=sep)

    def Thistle(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.THISTLE,sep=sep)

    def Plum(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PLUM,sep=sep)

    def Violet(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.VIOLET,sep=sep)

    def Magenta(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MAGENTA,sep=sep)

    def Orchid(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ORCHID,sep=sep)

    def MediumVioletRed(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MEDIUMVIOLETRED,sep=sep)

    def PaleVioletRed(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PALEVIOLETRED,sep=sep)

    def DeepPink(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DEEPPINK,sep=sep)

    def HotPink(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.HOTPINK,sep=sep)

    def LightPink(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTPINK,sep=sep)

    def Pink(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PINK,sep=sep)

    def AntiqueWhite(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ANTIQUEWHITE,sep=sep)

    def Beige(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BEIGE,sep=sep)

    def Bisque(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BISQUE,sep=sep)

    def BlanchedAlmond(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BLANCHEDALMOND,sep=sep)

    def Wheat(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.WHEAT,sep=sep)

    def CornSilk(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CORNSILK,sep=sep)

    def LemonChiffon(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LEMONCHIFFON,sep=sep)

    def LightGoldenRodYellow(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTGOLDENRODYELLOW,sep=sep)

    def LightYellow(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTYELLOW,sep=sep)

    def SaddleBrown(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SADDLEBROWN,sep=sep)

    def Sienna(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SIENNA,sep=sep)

    def Chocolate(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.CHOCOLATE,sep=sep)

    def Peru(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PERU,sep=sep)

    def SandyBrown(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SANDYBROWN,sep=sep)

    def BurlyWood(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BURLYWOOD,sep=sep)

    def Tan(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.TAN,sep=sep)

    def RosyBrown(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ROSYBROWN,sep=sep)

    def Moccasin(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MOCCASIN,sep=sep)

    def NavajoWhite(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.NAVAJOWHITE,sep=sep)

    def PeachPuff(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PEACHPUFF,sep=sep)

    def MistyRose(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MISTYROSE,sep=sep)

    def LavenderBlush(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LAVENDERBLUSH,sep=sep)

    def Linen(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LINEN,sep=sep)

    def OldLace(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.OLDLACE,sep=sep)

    def PapayaWhip(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.PAPAYAWHIP,sep=sep)

    def WeaShell(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.WEASHELL,sep=sep)

    def MintCream(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.MINTCREAM,sep=sep)

    def SlateGray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SLATEGRAY,sep=sep)

    def LightSlateGray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTSLATEGRAY,sep=sep)

    def LightSteelBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTSTEELBLUE,sep=sep)

    def Lavender(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LAVENDER,sep=sep)

    def FloralWhite(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.FLORALWHITE,sep=sep)

    def AliceBlue(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.ALICEBLUE,sep=sep)

    def GhostWhite(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GHOSTWHITE,sep=sep)

    def Honeydew(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.HONEYDEW,sep=sep)

    def Ivory(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.IVORY,sep=sep)

    def Azure(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.AZURE,sep=sep)

    def Snow(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SNOW,sep=sep)

    def Black(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.BLACK,sep=sep)

    def DimGray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DIMGRAY,sep=sep)

    def Gray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GRAY,sep=sep)

    def DarkGray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.DARKGRAY,sep=sep)

    def Silver(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.SILVER,sep=sep)

    def LightGray(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.LIGHTGRAY,sep=sep)

    def Gainsboro(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.GAINSBORO,sep=sep)

    def WhiteSmoke(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.WHITESMOKE,sep=sep)

    def White(self, *obj:tuple[Any, ...], sep:str=sep_) -> str:
        return self.custom(*obj,color=HtmlColorObjects.WHITE,sep=sep)