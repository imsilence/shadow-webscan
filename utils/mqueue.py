#encoding: utf-8

from queue import Queue as PyQueue

class Queue(PyQueue):

    def put(self, item):
        super(Queue, self).put(item, block=False)

    def get(self):
        return super(Queue, self).get(block=False)

    def empty(self):
        return super(Queue, self).empty()

    def size(self):
        return super(Queue, self).qsize()