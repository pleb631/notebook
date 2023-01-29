1.判断两个点是否在两点连线的同一侧，可以先求出直线的方程，然后求出每个点在直线的左边或右边，最后进行结论
```python
from scipy import optimize
#point1(x1,y1),point2(x2,y2) 拟合直线方程
x0 = [x1, x2]
y0 = [y1, y2]
A1, B1 = optimize.curve_fit(fx, x1, y0)[0]

#判断point与直线的关系
judge_value = A1 * x1 + B1 - y1
if  judge_value > 0:
    flag = 1 #在右边
elif judge_value<0：
    flag=-1 #在左边
else:
    flag=0#在直线上
```

2.计算角点的角度
```python
def caculateAngleByVec(self, vec1, vec2, vec_node):
    """
    Calculate the angle from vec_node to vec1 and vec_node to vec2
    param vec1: one point
    param vec2: another point
    param vec_node: Intersection point
    return sita: return the angle from  vec_node to vec1 and vec_node to vec2
    """
    vec_node2vec1 = vec1 - vec_node
    vec_node2vec2 = vec2 - vec_node
    L_vec_node2vec1 = np.sqrt(vec_node2vec1.dot(vec_node2vec1))
    L_vec_node2vec2 = np.sqrt(vec_node2vec2.dot(vec_node2vec2))
    cos_angle = vec_node2vec1.dot(vec_node2vec2) / (L_vec_node2vec1 * L_vec_node2vec2)
    sita = np.arccos(cos_angle)
    sita = sita * 180 / np.pi
    if sita < 0:
        sita +=180
    return sita
```