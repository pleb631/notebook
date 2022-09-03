


def iou(x1,y1, x2, y2, a1, b1, a2, b2):
    
    
	ax = max(x1, a1) # 相交区域左上角横坐标
	ay = max(y1, b1) # 相交区域左上角纵坐标
	bx = min(x2, a2) # 相交区域右下角横坐标
	by = min(y2, b2) # 相交区域右下角纵坐标
	
	area_N = (x2 - x1) * (y2 - y1)
	area_M = (a2 - a1) * (b2 - b1)
	
	w = bx - ax
	h = by - ay
	if w<=0 or h<=0:
		return 0 # 不相交返回0	
	area_X = w * h
	return area_X / (area_N + area_M - area_X)


