# -*- coding=utf-8 -*-

import maya.cmds as ma
import maya.mel as mel
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os

path = os.path.expanduser('~')
'C:/Users/mlinchun/Documents/maya/scripts/xiaolin_script'




def spring_start():
    # C:\Users\mlinchun\Documents\maya\scripts\xiaolin_script\springmagic
    # execfile(r'X:\Linchun\Linchun_Aesset\Maya\tools\springmagic\springMagic.py')

    sppath = path + "/maya/scripts/xiaolin_script/springmagic/springMagic.py"
    print(sppath)
    exec(compile(open(sppath).read(), sppath , 'exec'))


# C:\Users\mlinchun
# C:\Users\mlinchun\Documents\maya\scripts\xiaolin_script\mel


def blendshape_node(node1, node2):
    bl = ma.blendShape(node1, node2)
    if bl != "":
        if ':' in node2:
            blen = bl[0] + "." + node2.split(':')[-1]
        else:
            blen = bl[0] + "." + node2.split('|')[-1]

        print(blen)
        ma.setAttr(blen, 1)

    # setAttr "blendShape1.Cloth_01_WrapShap" 1;

    return bl


def blend_take():
    nodes = ma.ls(sl=1, dag=1, l=1, type=['mesh'])
    # '|group2|pCylinder1|pCylinderShape1'
    # print(nodes)
    name1 = []
    name2 = []
    fg = nodes[0].split("|")[1]
    # print(fg)
    for node in nodes:
        fg1 = node.split("|")[1]
        # print(fg1)
        if fg1 == fg:
            name1.append(node)
        else:
            name2.append(node)
    # print(name1)
    # print(name2)
    for na1 in name1:
        bl1 = na1.split("Shap")[0]
        com1 = bl1.split("|")[-1]
        # print('com1 = '+com1)

        # print(bl1)
        for na2 in name2:
            bl2 = na2.split("Shap")[0]
            com2 = bl2.split("|")[-1]
            # print('bl2'+bl2)
            # print('com2 = '+com2)
            if ':' in com1:
                comend1 = com1.split(':')[-1]

            else:
                comend1 = com1

            if ":" in com2:
                comend2 = com2.split(':')[-1]
            else:
                comend2 = com2

            if comend1 == comend2:
                # print(na1)
                try:
                    blend = blendshape_node(na1, na2)
                # print(blend)
                except:
                    blend = blendshape_node(com1, com2)
                break


def rand_color():
    mel_rand_color = """string $object[] = `ls -sl`;
        string $sel[]=`ls -sl`;
        for($objects in $sel)
        {
        float $f=rand(0,1);
        string $shaderName=`shadingNode -asShader  lambert`;
        string $shaderNameSG=`sets -renderable true -noSurfaceShader true -empty -name ($shaderName+"SG")`;
        connectAttr -f ($shaderName+".outColor") ($shaderNameSG+".surfaceShader");
        string $HsvName=`shadingNode -asUtility remapHsv`;
        connectAttr -force ($HsvName+".outColor") ($shaderName+".color");
        select -r $objects;
        sets -e -forceElement $shaderNameSG;
        setAttr ($HsvName+".color") -type double3 1 0.156 0.346322 ;
        setAttr ($HsvName+".hue[1].hue_FloatValue") $f;
        } """
    re = mel.eval(mel_rand_color)
    return re


def dyn_start():
    print(path)
    melpath = path + "/maya/scripts/xiaolin_script/mel/"
    dynpath = melpath + "dyn.mel"
    f = open(dynpath, "r",encoding="utf-8")
    mel_dyn = f.read()
    f.close()
    # print(mel_dyn)

    mel.eval(mel_dyn)


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()

    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QMainWindow):

    def __init__(self, parent=get_maya_main_window()):
        super(TestDialog, self).__init__(parent)
        # 窗口设置
        self.setWindowTitle("小林CFX工具箱")
        self.setFixedSize(300, 250)  # 设置窗口固定大小
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # 按钮设置
        self.btn_color = QtWidgets.QPushButton("物体随机上色")

        self.btn_bs = QtWidgets.QPushButton('一键融合变形')
        self.btn_dyn = QtWidgets.QPushButton("动力学管理器_by田静海")
        self.btn_spring = QtWidgets.QPushButton("飘带动力学_by动画大白")
        self.main_layout.addWidget(self.btn_color)
        self.main_layout.addWidget(self.btn_bs)
        self.main_layout.addWidget(self.btn_dyn)
        self.main_layout.addWidget(self.btn_spring)
        self.setCentralWidget(self.main_widget)

        # 按钮事件
        self.btn_color.clicked.connect(self.clicks_color)
        self.btn_bs.clicked.connect(self.clicks_bs)
        self.btn_dyn.clicked.connect(self.clicks_dyn)
        self.btn_spring.clicked.connect(self.clicks_spring)

    def clicks_color(self):
        rand_color()

    def clicks_bs(self):
        blend_take()

    def clicks_dyn(self):
        dyn_start()
        d.close()

    def clicks_spring(self):
        spring_start()
        d.close()


if __name__ == "__main__":
    d = TestDialog()
    d.show()
