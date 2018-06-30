from src.basic_block import Block
from queue import Queue
class Function:

    def __init__(self, List):
        self.queue = Queue()
        self.in_queue = set()
        List = List.splitlines()
        tmp_list = []
        for line in List:
            if line.strip() != '':
                tmp_list.append(line.lstrip())
        tmp_list = tmp_list[1:]
        for i in range(len(tmp_list)):
            if tmp_list[i][0] == '<':
                tmp_list[i] = '@@' + tmp_list[i]
        List = '\n'.join(tmp_list)
        
        self.name = List[:List.find('(') - 1]
        # print('Function: ' + self.name + ' detected, Creating basic blocks:')
        
        List = List.split('@@')
        self.blocklist = {}
        for blocks in List:
            block_obj = Block(blocks, self)
            self.blocklist[block_obj.id] = block_obj

        #Analysis of pred and succ
        # print('Basic blocks created, analyze pred and succ:')
        for bb in self.blocklist:
            for stats in self.blocklist[bb].stat:
                if stats[0:4] == 'goto':
                    if stats.find('(') == -1:
                        self.blocklist[bb].succ.append(stats[5:])
                        self.blocklist[stats[5:]].pred.append(self.blocklist[bb].id)
                    else:
                        self.blocklist[bb].succ.append(stats[5:stats.find('>')+1])
                        self.blocklist[stats[5:stats.find('>')+1]].pred.append(self.blocklist[bb].id)
            for i in range(len(List)):
                if i == 0:
                    self.blocklist['<bb 1>'].succ.append(self.blocklist[List[1][:List[1].find('>') + 1]].id)
                elif List[i][:List[i].find('>') + 1] == self.blocklist[bb].id:
                    if i + 1 < len(List):
                        self.blocklist[bb].succ.append(self.blocklist[List[i + 1][:List[i + 1].find('>') + 1]].id)
                    if i - 1 > 0:
                        self.blocklist[bb].pred.append(self.blocklist[List[i - 1][:List[i - 1].find('>') + 1]].id)
                    if i == 1:
                        self.blocklist[bb].pred.append('<bb 1>')

        for bb in self.blocklist:
            self.blocklist[bb].pred = list(set(self.blocklist[bb].pred))
            self.blocklist[bb].succ = list(set(self.blocklist[bb].succ))
            print(self.blocklist[bb].id, self.blocklist[bb].pred, self.blocklist[bb].succ)

    def start(self):
        self.queue.put(('<bb 1>','<bb 0>'))
        self.in_queue.add('<bb 1>')
        cnt = 0
        while not self.queue.empty():
            block,pred_id = self.queue.get()
            self.in_queue.remove(block)
            self.blocklist[block].in_to_out(pred_id)
            # cnt += 1
            # if cnt == 1000:
            #     break