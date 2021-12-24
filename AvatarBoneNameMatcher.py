# インポート
import sys, os
import bpy

# Leftなら0、Rなら1を返すよ。えらい。
def l_r_detect(name):
    if 'L' in name and 'R' not in name[-1] and 'right' not in name.lower() or 'left' in name.lower():
        return 0
    elif 'R' in name and 'L' not in name[-1] and 'left' not in name.lower() or 'right' in name.lower():
        return 1
    else:
        return -1


# 素体側ボーンの内、表記ゆれが多い奴だけを抽出して配列に格納するよ。例外に日々怯えているよ。
def init_bone_list():
    #リスト初期化
    boneNameList =  [[] for i in range(2)]
    # シーン中の全てのオブジェクト検索
    for ob in bpy.context.scene.objects:
        # オブジェクト内からアーマーチュアを検索
        if ob.type == 'ARMATURE':
            # Armatureという名称を使用しているものを親(素体側)とする
            if ob.name == 'Armature':
                # Armature内のBoneを検索
                for bone in ob.data.bones:
                    # Bone名の内、関係のありそうなもののみ取得。なんかいい感じに短くしたい
                    if 'shoulder' in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
                    elif 'arm' in bone.name.lower():
                        # upってパターンとupperのパターンを包括。例外ありそう
                        if 'up' in bone.name.lower():
                            boneNameList[l_r_detect(bone.name)].append(bone.name)
                        elif 'lower' in bone.name.lower():
                            boneNameList[l_r_detect(bone.name)].append(bone.name)
                        elif 'fore' in bone.name.lower():
                            boneNameList[l_r_detect(bone.name)].append(bone.name)
                        else:
                            boneNameList[l_r_detect(bone.name)].append(bone.name)                             
                    elif 'elbow' in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
                    elif 'hand' in bone.name.lower() and 'thumb' not in bone.name.lower() \
                        and 'index' not in bone.name.lower() \
                        and 'middle' not in bone.name.lower() \
                        and 'ring' not in bone.name.lower() \
                        and 'pinky' not in bone.name.lower() \
                        and 'support' not in bone.name.lower() \
                        and 'ribon' not in bone.name.lower() \
                        and 'ribbon' not in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
                    elif 'wrist' in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
                    elif 'leg' in bone.name.lower():
                        # upってパターンとupperのパターンを包括。例外ありそう
                        if 'up' in bone.name.lower():
                            boneNameList[l_r_detect(bone.name)].append(bone.name)
                        elif 'lower' in bone.name.lower():
                            boneNameList[l_r_detect(bone.name)].append(bone.name)
                        # Leg単体のパターンもあるらしい。もうわからん
                        else:
                            boneNameList[l_r_detect(bone.name)].append(bone.name)
                            # Leg単体の時はLeg = LowerLegになるので、入れ替えておかないと辛いことになる
                            boneNameList[l_r_detect(bone.name)][-1], boneNameList[l_r_detect(bone.name)][-2] = boneNameList[l_r_detect(bone.name)][-2], boneNameList[l_r_detect(bone.name)][-1]
                    elif 'knee' in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
                    elif 'foot' in bone.name.lower() or 'ankle' in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
                    # ToesもToeもまとめるならこれでいいかなって
                    elif 'toe' in bone.name.lower():
                        boneNameList[l_r_detect(bone.name)].append(bone.name)
    return boneNameList

# 素体のボーン名称に合わせて服側のボーン名称を変更するよ。力業だよ。
def change_name(parentList, targetNameA, targetNameB, targetNameC):
    for name in parentList:
        if targetNameA in name.lower():
            if targetNameB is None:
                return name
            elif targetNameC is None:
                if targetNameA in name.lower() and targetNameB in name.lower():
                    return name
            else:
                if targetNameA in name.lower() and targetNameB in name.lower() and targetNameC in name.lower():
                    return name
    return -1

# 服側のボーンを抽出してchenge_name()へ投げつけるよ。CUIだけならこれがある意味メイン関数だよ。
def change_bone_name():
    parentBoneList = init_bone_list()
    # 素体ボーンが特殊枠かどうかを確認するよ。具体的にはForeが含まれているか調べるよ
    flagArm = flagLeg = flagFoot = False
    for i in range(len(parentBoneList[0])):
        if 'fore' in parentBoneList[0][i].lower():
            flagArm = True
            if flagLeg is True:
                break
        elif 'lower' in parentBoneList[0][i].lower():
            flagLeg = True
            if flagArm is True:
                break
        elif 'ankle' in parentBoneList[0][i].lower():
            flagFoot = True
            if flagArm is True:
                break
#    print(parentBoneList)
    # シーン中の全てのオブジェクト検索
    for ob in bpy.context.scene.objects:
        # オブジェクト内からArmatureを検索
        if ob.type == 'ARMATURE':
            # Armatureという名称ではないものを検索(着せたい服側を指定したい)
            if ob.name != 'Armature':
                # Armature内のBoneを検索
                for bone in ob.data.bones:
                    # 各引数用の変数を初期化
                    nameA = nameB = nameC = ''
                    # Bone名の内、関係のありそうなもののみ取得して入れ替え。うーん、スパゲッティ。。。
                    # 例外。Ribbonとかよくあるよね
                    if 'ribbon' in bone.name.lower():
                            nameC = 'ribbon'            
                    elif 'shoulder' in bone.name.lower():
                        nameA = 'shoulder'
                    elif 'arm' in bone.name.lower():
                        nameA = 'arm'
                        if flagArm is False:
                            if 'up' in bone.name.lower():
                                nameB = 'up'
                                if 'twist' in bone.name.lower():
                                    nameC = 'twist'
                            elif 'lower' in bone.name.lower():
                                nameB = 'lower'
                                if 'twist' in bone.name.lower():
                                    nameC = 'twist'
                            elif 'fore' in bone.name.lower():
                                nameB = 'fore'
                        else:
                            if 'up' in bone.name.lower():
                                #nameB = 'up'
                                if 'twist' in bone.name.lower():
                                    nameB = 'twist'
                            elif 'lower' in bone.name.lower():
                                nameB = 'fore'
                                if 'twist' in bone.name.lower():
                                    nameC = 'twist'
                            elif 'fore' in bone.name.lower():
                                nameB = 'fore'
                    elif 'elbow' in bone.name.lower():
                        nameA = 'elbow'
                    elif 'hand' in bone.name.lower() and 'thumb' not in bone.name.lower() \
                        and 'index' not in bone.name.lower() \
                        and 'middle' not in bone.name.lower() \
                        and 'ring' not in bone.name.lower() \
                        and 'pinky' not in bone.name.lower() \
                        and 'support' not in bone.name.lower() \
                        and 'ribon' not in bone.name.lower() \
                        and 'ribbon' not in bone.name.lower():
                        nameA = 'hand'
                    elif 'wrist' in bone.name.lower():
                        nameA = 'wrist'
                    elif 'leg' in bone.name.lower():
                        nameA = 'leg'
                        if 'up' in bone.name.lower():
                            nameB = 'up'
                        elif 'lower' in bone.name.lower():
                            if flagLeg is True:
                                nameB = 'lower'
                        elif flagLeg is False:
                            nameB = 'lower'
                    elif 'knee' in bone.name.lower():
                        nameA = 'knee'
                    elif 'foot' in bone.name.lower():
                        nameA = 'foot'
                    elif 'ankle' in bone.name.lower():
                        if flagFoot is True:
                            nameA = 'ankle'
                        else:
                            nameA = 'foot'
                    #ToesもToeもまとめるならこれでいいかなって
                    elif 'toe' in bone.name.lower():
                        nameA = 'toe'
                    else:
                        nameA = nameB = nameC = ''
                        continue
#                    print('input is ' + bone.name + ', A is ' + nameA + ', B is ' + nameB + ', C is ' + nameC)
                    if l_r_detect(bone.name) >= 0:
                        if change_name(parentBoneList[l_r_detect(bone.name)], nameA, nameB, nameC) != -1:
                            print('input is ' + bone.name + ', output is ' + change_name(parentBoneList[l_r_detect(bone.name)], nameA, nameB, nameC))
#                           bone.name = change_name(parentBoneList[l_r_detect(bone.name)], nameA, nameB, nameC)
                        else:
                            print('kanashimi')

# 実行指定で呼び出されているかチェック
change_bone_name()
print('----------Done!----------')