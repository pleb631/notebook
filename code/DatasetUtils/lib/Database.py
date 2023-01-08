import os
import sqlite3
from glob import glob
import numpy as np
# import streamlit as st

class SQLiteDatabase:
    """SQLite数据库类

    Attributes:
        db_connector: connect, 数据库连接器
        cur: cursor, 数据库游标
    """
    def __init__(self, db_file_path):
        self.db_connector = sqlite3.connect(db_file_path, check_same_thread=False)
        self.cur = self.db_connector.cursor()

    def create_table(self):
        """创建新表
        """
        sql_text = '''CREATE TABLE images
            (imagePath TEXT,
            classID NUMBER,
            trackID TEXT,
            camSNID TEXT,
            frameNum INTEGER,
            time TEXT,
            identity TEXT,
            headShoulderBox TEXT,
            qualityScore REAL,
            PRIMARY KEY (imagePath)
            );'''
        self.cur.execute(sql_text)

        sql_text = '''CREATE TABLE classID2mergeID
            (classID NUMBER,
            mergeID NUMBER,
            PRIMARY KEY (classID)
            );'''
        self.cur.execute(sql_text)

    def insert_data(self, table_name, info):
        '''插入新数据

        Args:
            table_name: str, 按tracking id排序的内容
            info: str, 数据内容
        '''
        sql_text = 'INSERT INTO %s VALUES(%s)'%(table_name, info)
        self.cur.execute(sql_text)

    def clean_table(self, table_name):
        '''清空表

        Args:
            table_name: str, 按tracking id排序的内容
        '''
        sql_text = ' DELETE FROM %s'%(table_name)
        self.cur.execute(sql_text)

    def get_trackid_mergeid(self):
        '''在images表格中获取imagePath-trackID-classID-mergeID
        '''
        sql_text = "SELECT images.imagePath,images.trackID,images.classID, classID2mergeID.mergeID, images.time FROM images LEFT JOIN classID2mergeID ON images.classID == classID2mergeID.classID"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()

        return np.array(data)

    def getDistinctClassID(self):
        sql_text = "SELECT distinct classID FROM  images"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def getClassID2MergeID(self):
        sql_text = "SELECT * FROM  classID2mergeID"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).tolist()

    def get_cor_top1_classid(self, classid, thresh):
        '''获取得到每个classid与其他所有classid的相似度，过滤出大于阈值的，排序得出top1的classid
        '''
        sql_text = "SELECT * FROM(SELECT * FROM  cosmility where classid1==%d or classid2==%d and cosval>=%f) ORDER BY COSVAL DESC LIMIT 1" % (classid, classid, thresh)
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).tolist()

    def getAllMergeID(self, filter_badclass_flag = False):
        if not filter_badclass_flag:
            sql_text = "SELECT DISTINCT mergeID FROM  classID2mergeID"
        else:
            sql_text = "SELECT DISTINCT mergeID FROM  classID2mergeID LEFT JOIN badClassID ON classID2mergeID.classID == badClassID.classID WHERE badClassID.classID is NULL"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def get_cosim_state1(self):
        sql_text = "SELECT classid1, classid2, cosval FROM  cosmility where cosmility.mergestate==1"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data)

    def get_cosval_of_classid1_2(self, classid1, classid2):
        sql_text = "SELECT cosval FROM  cosmility where cosmility.classid1==%d AND cosmility.classid2==%d"%(classid1, classid2)
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def get_cosval_of_mergeid1_2(self, mergeid1, mergeid2, threshold):
        sql_text = "SELECT * FROM\
                                (SELECT * FROM  cosmility WHERE classid1 IN (SELECT classID FROM  classID2mergeID WHERE mergeID==%d) \
                                INTERSECT\
                                SELECT * FROM  cosmility WHERE classid2 IN (SELECT classID FROM  classID2mergeID WHERE mergeID==%d))\
                                AS mergeid_cosmility \
                                WHERE mergeid_cosmility.cosval>=%f" % (mergeid1, mergeid2, threshold)
        # sql_text = "SELECT cosval FROM  cosmility where cosmility.classid1==%d AND cosmility.classid2==%d AND cosmility.mergestate==%d"%(classid1, classid2, 1)
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).tolist()

    def get_sales_mergeid_list(self):
        sql_text = "SELECT DISTINCT mergeID FROM  salesMergeID"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def getTrackID2ClassID(self):
        sql_text = "select distinct trackID, classid from images"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).tolist()

    def getTrackIDofImagePath(self, imagePath):
        sql_text = "SELECT trackID FROM  images where instr(imagePath, '%s')>0"%(imagePath)
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def getClassIDofTrackID(self, trackID):
        sql_text = "SELECT distinct classID FROM  images where trackID == '%s'"%(trackID)
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).tolist()

    def getAllBadClassID(self):
        sql_text = "SELECT DISTINCT classID FROM  badClassID"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def getAllClassID(self):
        sql_text = "SELECT classID FROM  classID2mergeID"
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data).flatten().tolist()

    def getTopkClassid(self,classid1):
        sql_text = "SELECT *  FROM  cosmility where classid1 == {:d} ORDER BY cosval DESC LIMIT 5".format(classid1)
        self.cur.execute(sql_text)
        data = self.cur.fetchall()
        return np.array(data)

    def mergeClassID(self,classid1,classid2,Flag):
        if Flag:
            sql_text = "UPDATE cosmility  SET  mergestate = 1 WHERE classid1 == {:d} AND classid2 == {:d}".format(int(classid1),int(classid2))
        else:
            sql_text = "UPDATE cosmility  SET  mergestate = 0 WHERE classid1 == {:d} AND classid2 == {:d}".format(int(classid1),int(classid2))

        update_fail_flag = True
        while update_fail_flag:
            try:
                self.cur.execute(sql_text)
                update_fail_flag = False
            except sqlite3.Error:
                print('Error:', int(classid1), int(classid2))
                # st.error(int(classid1), '<->', int(classid2), '合并关系更新失败！请重试！')

    def getImageInfoByMergeID(self,mergeID = None, filter_badclass_flag = False):
        if mergeID is not None and filter_badclass_flag:
            sql_text = "SELECT nonbad_images.imagePath,nonbad_images.trackID,nonbad_classID2mergeID.mergeID, nonbad_images.images_classID \
                                    FROM (SELECT images.classID as images_classID,images.imagePath as imagePath,images.trackID as trackID FROM images LEFT JOIN badClassID ON images.classID == badClassID.classID WHERE badClassID.classID is NULL) as nonbad_images \
                                    LEFT JOIN (SELECT classID2mergeID.classID as classID2mergeID_classID,classID2mergeID.mergeID as mergeID FROM classID2mergeID LEFT JOIN badClassID ON classID2mergeID.classID == badClassID.classID WHERE badClassID.classID is NULL) as nonbad_classID2mergeID \
                                    ON nonbad_images.images_classID == nonbad_classID2mergeID.classID2mergeID_classID \
                                    WHERE nonbad_classID2mergeID.mergeID == {:d}".format(mergeID)
        elif mergeID is not None and (not filter_badclass_flag):
            sql_text = "SELECT images.imagePath,images.trackID,classID2mergeID.mergeID,images.classID FROM images LEFT JOIN classID2mergeID ON images.classID == classID2mergeID.classID WHERE classID2mergeID.mergeID == {:d}".format(
                mergeID)
        else:
            sql_text = "SELECT images.imagePath,images.trackID,classID2mergeID.mergeID,images.classID FROM images LEFT JOIN classID2mergeID ON images.classID == classID2mergeID.classID"

        self.cur.execute(sql_text)
        data = self.cur.fetchall()

        return np.array(data)

    def getImageInfoByClassID(self,classID = None):
        if classID is not None:
            sql_text = "SELECT images.imagePath,images.trackID,classID2mergeID.mergeID FROM images LEFT JOIN classID2mergeID ON images.classID == classID2mergeID.classID WHERE classID2mergeID.classID == {:d}".format(
                classID)
        else:
            sql_text = "SELECT images.imagePath,images.trackID,classID2mergeID.mergeID FROM images LEFT JOIN classID2mergeID ON images.classID == classID2mergeID.classID"
        self.cur.execute(sql_text)

        data = self.cur.fetchall()

        return np.array(data)

    # def __del__(self):
    #     self.db_connector.commit()
    #     self.cur.close()
    #     # self.conn.close()
