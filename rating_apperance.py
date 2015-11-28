#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $File: hello.py

# In this tutorial, you will learn how to call Face ++ APIs and implement a
# simple App which could recognize a face image in 3 candidates.
# 在本教程中，您将了解到Face ++ API的基本调用方法，并实现一个简单的App，用以在3
# 张备选人脸图片中识别一个新的人脸图片。

# You need to register your App first, and enter you API key/secret.
# 您需要先注册一个App，并将得到的API key和API secret写在这里。

def init():
  import sys
  import os
  import os.path
  if sys.version_info.major != 2:
    sys.exit('Python 2 is required to run this program')

  fdir = None
  if hasattr(sys, "frozen") and \
     sys.frozen in ("windows_exe", "console_exe"):
    fdir = os.path.dirname(os.path.abspath(sys.executable))
    sys.path.append(fdir)
    fdir = os.path.join(fdir, '..')
  else:
    fdir = os.path.dirname(__file__)

  with open(os.path.join(fdir, 'apikey.cfg')) as f:
    exec(f.read())

  srv = locals().get('SERVER')
  from facepp import API
  return API(API_KEY, API_SECRET, srv = srv)

import math
def distance(x1,y1,x2,y2):
  """计算两点之间的距离"""
  return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
  
# Import system libraries and define helper functions
# 导入系统库并定义辅助函数
import time
from pprint import pformat
def print_result(hint, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])

# First import the API class from the SDK
# 首先，导入SDK中的API类并初始化
api = init()
del init

from facepp import File
import math

def rating_apperance(face):
  """传说中的三庭五眼计算颜值"""
  # 笑容参数计算
  smile = int(face['attribute']['smiling']['value'])
  if smile < 20:
    smile = -10
  else:
    smile = int(smile/10)
  
  # 面部轮廓检测
  landmark = api.detection.landmark(face_id = face['face_id'])
  landmark = landmark['result'][0]['landmark']
  #print_result('面部轮廓信息',landmark)

  # 眉头间的距离
  dis_l_r_eyebrows = \
  distance(landmark['left_eyebrow_right_corner']['x'],landmark['left_eyebrow_right_corner']['y'],landmark['right_eyebrow_left_corner']['x'],landmark['right_eyebrow_left_corner']['y'])
  
  # 眉毛中点到鼻子最低处的距离
  loc_m_eyebrow = {'x':(landmark['right_eyebrow_left_corner']['x']-landmark['left_eyebrow_right_corner']['x'])/2.0 + \
                   landmark['left_eyebrow_right_corner']['x'],\
                   'y':(landmark['right_eyebrow_left_corner']['y']-landmark['left_eyebrow_right_corner']['y'])/2.0 + \
                   landmark['left_eyebrow_right_corner']['y']}

  dis_m_eyebrow_lowest_nose = \
  distance(landmark['nose_contour_lower_middle']['x'],landmark['nose_contour_lower_middle']['y'],loc_m_eyebrow['x'],loc_m_eyebrow['y'])

  # 眼角之间的距离
  dis_l_r_eyes = \
  distance(landmark['left_eye_right_corner']['x'],landmark['left_eye_right_corner']['y'],landmark['right_eye_left_corner']['x'],landmark['right_eye_left_corner']['y'])

  # 鼻子宽
  width_nose = distance(landmark['nose_left']['x'],landmark['nose_left']['y'],landmark['nose_right']['x'],landmark['nose_right']['y'])

  # 脸宽
  width_face = \
  distance(landmark['contour_left1']['x'],landmark['contour_left1']['y'],landmark['contour_right1']['x'],landmark['contour_right1']['y'])

  # 下巴到鼻子最低处的距离
  dis_chin_lowest_nose = \
  distance(landmark['contour_chin']['x'],landmark['contour_chin']['y'],landmark['nose_contour_lower_middle']['x'],landmark['nose_contour_lower_middle']['y'])

  # 眼睛的宽度
  width_l_eye = \
  distance(landmark['left_eye_left_corner']['x'],landmark['left_eye_left_corner']['y'],landmark['left_eye_right_corner']['x'],landmark['left_eye_right_corner']['y'])

  width_r_eye = \
  distance(landmark['right_eye_left_corner']['x'],landmark['right_eye_left_corner']['y'],landmark['right_eye_right_corner']['x'],landmark['right_eye_right_corner']['y'])

  # 嘴巴的宽度
  width_mouth = \
  distance(landmark['mouth_left_corner']['x'],landmark['mouth_left_corner']['y'],landmark['mouth_right_corner']['x'],landmark['mouth_right_corner']['y'])

  # 嘴巴处脸的宽度
  width_face_near_mouth = \
  distance(landmark['contour_left6']['x'],landmark['contour_left6']['y'],landmark['contour_right6']['x'],landmark['contour_right6']['y'])

  # 颜值计算步骤
  full_mark,minus_mark = 100,0

  # 眼角距离约为脸宽的1/5左右
  minus_mark += math.fabs(dis_l_r_eyes/width_face*100 - 25)

  # 鼻子宽约为脸宽的1/5左右
  minus_mark += math.fabs(width_nose/width_face*100 - 25)

  # 眼睛的宽度约为脸宽的1/5左右
  minus_mark += math.fabs((width_l_eye + width_r_eye)/2/width_face*100 - 25)

  # 嘴巴宽度应为同一脸部宽度的1/2
  minus_mark += math.fabs(width_mouth/width_face_near_mouth*100 - 50)

  # 下巴到鼻子下方的高度，应该和眉毛中点到鼻子下方的距离相同
  minus_mark += math.fabs(dis_m_eyebrow_lowest_nose - dis_chin_lowest_nose)

  # 最后的得分
  final_mark = full_mark - int(minus_mark) + smile 

  print "颜值计算结果：%s" % final_mark
  
# from local directory
#url = r'/Users/vincent/Others/pics_face/fanbingbing.jpg'
url = r'/Users/vincent/Others/pics_face/testpic/IMG_4029.PNG'
def main(url):
  print '正在上传图片并计算...'
  img = File(url)
  rst = api.detection.detect(img = img)
  if rst['face'] and len(rst['face']) == 1:
    # 检测到人脸
    print_result("人脸检测结果",rst)
    face = rst['face'][0]
    rating_apperance(face)
  else:
    # 没有识别出人脸
    print '识别人脸失败'

"""                                                
# Here are the person names and their face images
# 人名及其脸部图片
IMAGE_DIR = 'http://cn.faceplusplus.com/static/resources/python_demo/'
PERSONS = [
    ('Jim Parsons', IMAGE_DIR + '1.jpg'),
    ('Leonardo DiCaprio', IMAGE_DIR + '2.jpg'),
    ('Andy Liu', IMAGE_DIR + '3.jpg')
]
TARGET_IMAGE = IMAGE_DIR + '4.jpg'

# Step 1: Detect faces in the 3 pictures and find out their positions and
# attributes
# 步骤1：检测出三张输入图片中的Face，找出图片中Face的位置及属性

FACES = {name: api.detection.detect(url = url)
        for name, url in PERSONS}

for name, face in FACES.iteritems():
    print_result(name, face)


# Step 2: create persons using the face_id
# 步骤2：引用face_id，创建新的person
for name, face in FACES.iteritems():
    rst = api.person.create(
            person_name = name, face_id = face['face'][0]['face_id'])
    print_result('create person {}'.format(name), rst)

# Step 3: create a new group and add those persons in it
# 步骤3：.创建Group，将之前创建的Person加入这个Group
rst = api.group.create(group_name = 'test')
print_result('create group', rst)
rst = api.group.add_person(group_name = 'test', person_name = FACES.iterkeys())
print_result('add these persons to group', rst)

# Step 4: train the model
# 步骤4：训练模型
rst = api.train.identify(group_name = 'test')
print_result('train', rst)
# wait for training to complete
# 等待训练完成
rst = api.wait_async(rst['session_id'])
print_result('wait async', rst)

# Step 5: recognize face in a new image
# 步骤5：识别新图中的Face
rst = api.recognition.identify(group_name = 'test', url = TARGET_IMAGE)
print_result('recognition result', rst)
print '=' * 60
print 'The person with highest confidence:', \
        rst['face'][0]['candidate'][0]['person_name']

# Finally, delete the persons and group because they are no longer needed
# 最终，删除无用的person和group
api.group.delete(group_name = 'test')
api.person.delete(person_name = FACES.iterkeys())

# Congratulations! You have finished this tutorial, and you can continue
# reading our API document and start writing your own App using Face++ API!
# Enjoy :)
# 恭喜！您已经完成了本教程，可以继续阅读我们的API文档并利用Face++ API开始写您自
# 己的App了！
# 旅途愉快 :)
"""
