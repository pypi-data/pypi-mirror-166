#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class FileUtils(object):

    def __init__(self, file_path):
        """
        :param file_path:   磁盘文件路径
        """
        self._file_path = file_path
        self._path, self._file_name = os.path.split(self._file_path)
        self._path = os.path.abspath(self._path)
        self._shot_name, self._extension = os.path.splitext(self._file_name)

    def read(self):
        s: dict = {
            'filepath': self.filepath,
            'path': self.path,
            'filename': self.filename,
            'shotname': self.shotname,
            'extension': self.extension,
        }
        return str(s).replace('\'', '"')

    def stat(self):
        """
        执行一个系统 stat 的调用
        return :
            st_mode: inode 保护模式
            st_ino: inode 节点号。
            st_dev: inode 驻留的设备。
            st_nlink: inode 的链接数。
            st_uid: 所有者的用户ID。
            st_gid: 所有者的组ID。
            st_size: 普通文件以字节为单位的大小；包含等待某些特殊文件的数据。
            st_atime: 上次访问的时间。
            st_mtime: 最后一次修改的时间。
            st_ctime: 由操作系统报告的"ctime"。在某些系统上（如Unix）是最新的元数据更改的时间，在其它系统上（如Windows）是创建时间（详细信息参见平台的文档）。
        """
        return os.stat(self.filepath)


    def isfile(self):
        """当前是否为文件"""
        return os.path.isfile(self.filepath)

    @property
    def filepath(self):
        """获取磁盘文件完整路径，虚拟路径转为完整路径"""
        return '{}{}{}'.format(self._path, os.sep, self.filename)

    @property
    def filesize(self):
        return os.path.getsize(self.filepath)

    @property
    def path(self):
        """获取磁盘文件保存绝对地址"""
        return self._path

    @property
    def filename(self):
        """获取磁盘文件包含扩展名的文件名"""
        return self._file_name

    @property
    def shotname(self):
        """获取磁盘文件不包含扩展名的文件名"""
        return self._shot_name

    @property
    def extension(self):
        """获取磁盘文件的扩展名,包含."""
        return self._extension

    def exists(self):
        """
        判断存放图片的文件夹是否存在
        """
        if self._path is None:
            return False
        return os.path.exists(self._path)

    def makedirs(self):
        """
        判断存放文件夹是否存在,若文件夹不存在就创建
        """
        if self._path is None:
            return
        if not self.exists():
            os.makedirs(self._path)

    def del_file(self):
        """
        删除磁盘文件
        """
        if self._file_path is None:
            return
        if os.path.exists(self._file_path):
            os.remove(self._file_path)


if __name__ == '__main__':
    pass
