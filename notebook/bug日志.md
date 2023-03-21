# python

## opencv

### imread,imwrite读写入图片失败

原因1：俩函数不支持中文路径
方案1：用imdecode/imencode替代，见[文档](/notebook/api/cv2.md)
方案2：用PIL包替代
