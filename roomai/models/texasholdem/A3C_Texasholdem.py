import multiprocessing
import os
import threading

import numpy as np
import tensorflow as tf

try:
    import gym
except:
    os.system('pip install gym')
import shutil
import roomai
from roomai.games.texasholdem import *
from roomai.games.common import RandomPlayer
import matplotlib.pyplot as plt

OUTPUT_GRAPH = True
LOG_DIR = './log'
MODEL_DIR = './checkpoint/TexasHoldemModel'
N_WORKERS = multiprocessing.cpu_count()
MAX_GLOBAL_EP = 100000
GLOBAL_NET_SCOPE = 'Global_Net'
UPDATE_GLOBAL_ITER = 4
TEST_STEP = 100
GAMMA = 0.9
ENTROPY_BETA = 0.001
LR_A = 0.0001  # learning rate for actor
LR_C = 0.0001  # learning rate for critic
GLOBAL_RUNNING_R = []
GLOBAL_EP = 0
TEST_STATE = []
TEST_R = []

N_A = 5
action_dict= {"Fold":0, "Check":1, "Call":2, "Raise":3, "Allin":4}
OPT_A = tf.train.RMSPropOptimizer(LR_A, name='RMSPropA')
OPT_C = tf.train.RMSPropOptimizer(LR_C, name='RMSPropC')


class ACNet(object):
    def __init__(self, scope, SESS=None, globalAC=None):
        self.SESS = SESS
        if scope == GLOBAL_NET_SCOPE:  # get global network
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, [None, 14, 8, 1], 'S')
                self.a_params, self.c_params = self._build_net(scope)[-2:]
        else:  # local net, calculate losses
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, [None, 14, 8, 1], 'S')
                self.a_his = tf.placeholder(tf.int32, [None, ], 'A')
                self.v_target = tf.placeholder(tf.float32, [None, 1], 'Vtarget')
                self.a_prob, self.v, self.a_params, self.c_params = self._build_net(scope)

                td = tf.subtract(self.v_target, self.v, name='TD_error')
                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))

                with tf.name_scope('a_loss'):
                    log_prob = tf.reduce_sum(
                        tf.log(tf.clip_by_value(self.a_prob, 1e-8, 1.0)) * tf.one_hot(self.a_his, N_A,
                                                                dtype=tf.float32), axis=1,keep_dims=True)
                    exp_v = log_prob * tf.stop_gradient(td)
                    entropy = -tf.reduce_sum(self.a_prob * tf.log(tf.clip_by_value(self.a_prob, 1e-8, 1.0)), axis=1, keep_dims=True)  # encourage exploration
                    self.exp_v = ENTROPY_BETA * entropy + exp_v
                    self.a_loss = tf.reduce_mean(-self.exp_v)

                with tf.name_scope('local_grad'):
                    self.a_grads = tf.gradients(self.a_loss, self.a_params)
                    self.c_grads = tf.gradients(self.c_loss, self.c_params)

            with tf.name_scope('sync'):
                with tf.name_scope('pull'):
                    self.pull_a_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, globalAC.a_params)]
                    self.pull_c_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, globalAC.c_params)]
                with tf.name_scope('push'):
                    self.update_a_op = OPT_A.apply_gradients(zip(self.a_grads, globalAC.a_params))
                    self.update_c_op = OPT_C.apply_gradients(zip(self.c_grads, globalAC.c_params))

    def _build_net(self, scope):
        w_init = tf.truncated_normal_initializer(0.,.05)
        with tf.variable_scope('actor'):
            a_conv = tf.layers.conv2d(self.s,filters=64,kernel_size=[5,5],strides=1,padding='SAME',name='aconv')
            a_pool = tf.layers.max_pooling2d(a_conv,pool_size=[4,4],strides=2)
            a_flat = tf.reshape(a_pool,[-1, 6 * 3 * 64])
            a_prob = tf.layers.dense(a_flat, N_A, tf.nn.softmax, kernel_initializer=w_init, name='ap')
        with tf.variable_scope('critic'):
            c_conv = tf.layers.conv2d(self.s, filters=64,kernel_size=[5,5], strides=1, padding='SAME', name='cconv')
            c_pool = tf.layers.max_pooling2d(c_conv, pool_size=[4,4],strides=2)
            c_flat = tf.reshape(c_pool, [-1, 6 * 3 * 64])
            v = tf.layers.dense(c_flat, 1, kernel_initializer=w_init, name='v')  # state value
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
        return a_prob, v, a_params, c_params

    def update_global(self, feed_dict):  # run by a local
        self.SESS.run([self.update_a_op, self.update_c_op], feed_dict)  # local grads applies to global net

    def pull_global(self):  # run by a local
        self.SESS.run([self.pull_a_params_op, self.pull_c_params_op])

    def choose_action(self, s, actions, workid):  # run by a local
        prob_weights = self.SESS.run(self.a_prob, feed_dict={self.s: s[np.newaxis, :]})
        all = 0.0
        for option in actions:
            all += prob_weights[0][action_dict[option]]
        if (all > 1e-8):
            randindex = np.random.choice(len(actions), p=[prob_weights[0][action_dict[option]] / all for option in actions])
        else:
            randindex = np.random.choice(len(actions))
        return actions[randindex]

    def action_prob(self, s):
        return self.SESS.run(self.a_prob, feed_dict={self.s: s[np.newaxis, :]})

class Worker(object):
    def __init__(self, name, sess, coord, globalAC):
        self.num_normal_players = 2
        self.params = {"param_num_normal_players": 2,
                  "param_init_chips": [100,100],
                  "param_big_blind_bet": 20, "backward_enable": True}
        self.env = roomai.games.texasholdem.TexasHoldemEnv()
        self.name = name
        self.random_player = RandomPlayer()
        self.chance_player = roomai.games.common.RandomPlayerChance()
        self.AC = ACNet(name, sess, globalAC)
        self.SESS = sess
        self.COORD = coord

    def work(self):
        global GLOBAL_RUNNING_R, GLOBAL_EP
        if GLOBAL_EP % 100 == 0:
            print(GLOBAL_EP)
        total_step = 1
        workid = int(str(self.name).split("_")[1])
        buffer_s, buffer_a, buffer_r = [], [], []
        while not self.COORD.should_stop() and GLOBAL_EP < MAX_GLOBAL_EP:
            infos, public, person_states, private_state, _ = self.env.init(self.params)
            self.random_player.receive_info(infos[1])
            self.chance_player.receive_info(infos[2])
            ep_r = 0
            while public[-1].is_terminal == False:
                turn = public[-1].turn
                # print(turn)
                if turn == 0:# A3C learner
                    # for normalcard in infos[0].person_state_history[-1].hand_cards:
                    #     print(normalcard.point_rank)
                    s = np.zeros((14,8,1))
                    if(public[-1].param_dealer_id==0):
                        for card in infos[0].public_state_history[-1].public_cards:
                            s[card.point_rank,card.suit_rank, 0] = 1
                        for card in infos[0].person_state_history[-1].hand_cards:
                            s[card.point_rank, card.suit_rank, 0] = 1
                    else:
                        for card in infos[0].public_state_history[-1].public_cards:
                            s[card.point_rank,card.suit_rank+4, 0] = 1
                        for card in infos[0].person_state_history[-1].hand_cards:
                            s[card.point_rank, card.suit_rank+4, 0] = 1
                    available_action = dict()
                    available_option = []
                    for action in list(infos[0].person_state_history[-1].available_actions.values()):
                        option = action.option
                        if option not in available_option:
                            available_option.append(option)
                            available_action[option] = action
                    a = self.AC.choose_action(s, available_option, workid)
                    action = available_action[a]
                    buffer_s.append(s)
                    buffer_a.append(action_dict[a])
                    buffer_r.append(0)
                    # print("action0", action.option)
                elif turn == 1: # random player
                    # # a3c player
                    # s = np.zeros((14, 8, 1))
                    # if (public[-1].param_dealer_id == 1):
                    #     for normalcard in infos[1].public_state_history[-1].public_cards:
                    #         s[normalcard.point_rank, normalcard.suit_rank, 0] = 1
                    #     for normalcard in infos[1].person_state_history[-1].hand_cards:
                    #         s[normalcard.point_rank, normalcard.suit_rank, 0] = 1
                    # else:
                    #     for normalcard in infos[1].public_state_history[-1].public_cards:
                    #         s[normalcard.point_rank, normalcard.suit_rank + 4, 0] = 1
                    #     for normalcard in infos[1].person_state_history[-1].hand_cards:
                    #         s[normalcard.point_rank, normalcard.suit_rank + 4, 0] = 1
                    # available_action = dict()
                    # available_option = []
                    # for action in list(infos[1].person_state_history[-1].available_actions.values()):
                    #     option = action.option
                    #     if option not in available_option:
                    #         available_option.append(option)
                    #         available_action[option] = action
                    # a = self.AC.choose_action(s, available_option, workid)
                    # action = available_action[a]
                    # # random player
                    action = self.random_player.take_action()
                    print("action1:", action.option)
                else:  # chance player
                    action = self.chance_player.take_action()
                infos, public, persons, private, _ = self.env.forward(action)
                self.random_player.receive_info(infos[1])
                self.chance_player.receive_info(infos[2])
            if(len(buffer_r) == 0):continue
            # print("score", public[-1].scores[0])
            buffer_r[-1] = public[-1].scores[0]
            ep_r += buffer_r[-1]
            v_s_ = 0  # terminal
            buffer_v_target = []
            for r in buffer_r[::-1]:  # reverse buffer r
                v_s_ = r + GAMMA * v_s_
                buffer_v_target.append(v_s_)
            buffer_v_target.reverse()

            buffer_s, buffer_a, buffer_v_target = np.stack(buffer_s,axis=0), np.array(buffer_a), np.vstack(
                buffer_v_target)
            feed_dict = {
                self.AC.s: buffer_s,
                self.AC.a_his: buffer_a,
                self.AC.v_target: buffer_v_target,
            }
            self.AC.update_global(feed_dict)

            buffer_s, buffer_a, buffer_r = [], [], []
            self.AC.pull_global()
            if len(GLOBAL_RUNNING_R) == 0:  # record running episode reward
                GLOBAL_RUNNING_R.append(ep_r)
            else:
                GLOBAL_RUNNING_R.append(0.99 * GLOBAL_RUNNING_R[-1] + 0.01 * ep_r)

            # if len(rewardlist[workid]) == 0:  # record running episode reward
            #     rewardlist[workid].append(ep_r)
            # else:
            #     rewardlist[workid].append(0.99 * rewardlist[workid][-1] + 0.01 * ep_r)
            print(
                self.name,
                "Ep:", GLOBAL_EP,
                "| Ep_r: %.3f" % GLOBAL_RUNNING_R[-1],
                  )
            GLOBAL_EP += 1


class A3C_Texasholdem(object):
    def __init__(self):
        self.graph = tf.Graph()
        with self.graph.as_default() as graph:
            self.sess = tf.Session()
            self.COORD = tf.train.Coordinator()
            with tf.device("/cpu:0"):
                self.GLOBAL_AC = ACNet(GLOBAL_NET_SCOPE, self.sess)  # we only need its params
                self.workers = []
                # Create worker
                for i in range(N_WORKERS):
                    i_name = 'W_%i' % i  # worker name
                    self.workers.append(Worker(i_name, self.sess, self.COORD, self.GLOBAL_AC))
            self.sess.run(tf.global_variables_initializer())
            self.saver = tf.train.Saver(max_to_keep=1)
            self.saver.save(self.sess, MODEL_DIR)

            if OUTPUT_GRAPH:
                if os.path.exists(LOG_DIR):
                    shutil.rmtree(LOG_DIR)
                tf.summary.FileWriter(LOG_DIR, self.sess.graph)

    def train(self):
        with tf.variable_scope('sifaxie_a3cmodel'):
            worker_threads = []
            for worker in self.workers:
                job = lambda: worker.work()
                t = threading.Thread(target=job)
                t.start()
                worker_threads.append(t)
            self.COORD.join(worker_threads)
            plt.plot(np.arange(len(GLOBAL_RUNNING_R)), GLOBAL_RUNNING_R)
            # for i in range(len(rewardlist)):
            #     with open("reward_"+str(i)+".csv", "w") as f:
            #         for line in rewardlist[i]:
            #             f.write(str(line) + "\n")
            #     with open("prob_" + str(i) + ".csv", "w") as f:
            #         for line in problist[i]:
            #             f.write(",".join(map(str, line)) + "\n")

            plt.xlabel('step')
            plt.ylabel('Total moving reward')
            plt.show()


    def load_model(self):

        self.saver = tf.train.import_meta_graph("./checkpoint/TexasHoldemModel.meta")
        self.saver.restore(self.sess, tf.train.latest_checkpoint("./checkpoint"))

    def choose_action(self, s, action):
        actions = dict()
        for work in self.workers:
            a = work.AC.choose_action(s, action)
            if (a in actions.keys()):
                actions[a] += 1
            else:
                actions[a] = 1
        action_list = [[v[1], v[0]] for v in actions.items()]
        action_list.sort(key=lambda x: -x[0])
        return (action_list[0][1])

    def predict_actions(self, s):
        prob = self.GLOBAL_AC.action_prob(s)
        return prob


if __name__ == "__main__":
    ysj = A3C_Texasholdem()
    ysj.train()
    # ysj.load_model()
    # print(ysj.workers[0].name)


