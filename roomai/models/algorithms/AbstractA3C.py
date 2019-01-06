#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Author  : SiFaXie
# @Date    : 2018/12/23
# @Email   : sifaxie@tencent.com
# @File    : AbstractA3C.py
# @Desc    : The abstract class of A3C

import multiprocessing
import os
import threading

import numpy as np
import tensorflow as tf

import shutil
import roomai
from roomai.games.texasholdem import *
from roomai.games.common import A3CPlayer
import matplotlib.pyplot as plt

GLOBAL_RUNNING_R = []
GLOBAL_EP = 0

class ACNet(object):
    '''
        The abstract class of AC Net
    '''

    def __init__(self, scope,
                 params,
                 state_spec=[None, 14, 8, 1],
                 N_A=5,
                 SESS=None,
                 globalAC=None
                 ):
        '''

        :param self:
        :param scope: Distinguish master or worker
        :param SESS:
        :param globalAC:
        :return:
        '''
        self.SESS = SESS
        self.ENTROPY_BETA = params['ENTROPY_BETA']
        self.LR_A = params['LR_A']
        self.LR_C = params['LR_C']
        self.N_A = N_A
        self.OPT_A = tf.train.RMSPropOptimizer(self.LR_A, name='RMSPropA')
        self.OPT_C = tf.train.RMSPropOptimizer(self.LR_C, name='RMSPropC')

        if scope == 'Global_Net':  # get global network
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, state_spec, 'S')
                self.a_params, self.c_params = self._build_net(scope)[-2:]
        else:  # local net, calculate losses
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, state_spec, 'S')
                self.a_his = tf.placeholder(tf.int32, [None, ], 'A')
                self.v_target = tf.placeholder(tf.float32, [None, 1], 'Vtarget')
                self.a_prob, self.v, self.a_params, self.c_params = self._build_net(scope)

                td = tf.subtract(self.v_target, self.v, name='TD_error')
                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))

                with tf.name_scope('a_loss'):
                    log_prob = tf.reduce_sum(
                        tf.log(tf.clip_by_value(self.a_prob, 1e-8, 1.0)) * tf.one_hot(self.a_his, self.N_A,
                                                dtype=tf.float32), axis=1, keep_dims=True)
                    exp_v = log_prob * tf.stop_gradient(td)
                    entropy = -tf.reduce_sum(self.a_prob * tf.log(tf.clip_by_value(self.a_prob, 1e-8, 1.0)), axis=1,
                                             keep_dims=True)  # encourage exploration
                    self.exp_v = self.ENTROPY_BETA * entropy + exp_v
                    self.a_loss = tf.reduce_mean(-self.exp_v)

                with tf.name_scope('local_grad'):
                    self.a_grads = tf.gradients(self.a_loss, self.a_params)
                    self.c_grads = tf.gradients(self.c_loss, self.c_params)

            with tf.name_scope('sync'):
                with tf.name_scope('pull'):
                    self.pull_a_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.a_params, globalAC.a_params)]
                    self.pull_c_params_op = [l_p.assign(g_p) for l_p, g_p in zip(self.c_params, globalAC.c_params)]
                with tf.name_scope('push'):
                    self.update_a_op = self.OPT_A.apply_gradients(zip(self.a_grads, globalAC.a_params))
                    self.update_c_op = self.OPT_C.apply_gradients(zip(self.c_grads, globalAC.c_params))

    def _build_net(self, scope):
        '''

        :param self:
        :param scope:
        :return:
        '''
        w_init = tf.truncated_normal_initializer(0., .05)
        with tf.variable_scope('actor'):
            a_conv = tf.layers.conv2d(self.s, filters=64, kernel_size=[5, 5], strides=1, padding='SAME', name='aconv')
            a_pool = tf.layers.max_pooling2d(a_conv, pool_size=[4, 4], strides=2)
            a_flat = tf.reshape(a_pool, [-1, 6 * 3 * 64])
            a_prob = tf.layers.dense(a_flat, self.N_A, tf.nn.softmax, kernel_initializer=w_init, name='ap')
        with tf.variable_scope('critic'):
            c_conv = tf.layers.conv2d(self.s, filters=64, kernel_size=[5, 5], strides=1, padding='SAME', name='cconv')
            c_pool = tf.layers.max_pooling2d(c_conv, pool_size=[4, 4], strides=2)
            c_flat = tf.reshape(c_pool, [-1, 6 * 3 * 64])
            v = tf.layers.dense(c_flat, 1, kernel_initializer=w_init, name='v')  # state value
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/actor')
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope + '/critic')
        return a_prob, v, a_params, c_params


    def update_global(self, feed_dict):  # run by a local
        self.SESS.run([self.update_a_op, self.update_c_op], feed_dict)  # local grads applies to global net

    def pull_global(self):  # run by a local
        self.SESS.run([self.pull_a_params_op, self.pull_c_params_op])

    def choose_action(self, s, available_actions, action_dict):
        '''

        :param s: state_spec
        :param available_actions:
        :param action_dict: action's index
        :return:
        '''
        prob_weights = self.SESS.run(self.a_prob, feed_dict={self.s: s[np.newaxis, :]})
        all = 0.0
        for option in available_actions:
            all += prob_weights[0][action_dict[option]]
        if (all > 1e-8):
            randindex = np.random.choice(len(available_actions),
                         p=[prob_weights[0][action_dict[option]] / all for option in available_actions])
        else:
            randindex = np.random.choice(len(available_actions))
        return available_actions[randindex]

    def action_prob(self, s):
        return self.SESS.run(self.a_prob, feed_dict={self.s: s[np.newaxis, :]})


class Worker(object):
    def __init__(self, name,
                 sess,
                 coord,
                 ACNet,
                 params):
        self.name = name
        self.params = params
        self.AC = ACNet
        self.SESS = sess
        self.COORD = coord
        self.gamma = params['GAMMA']
        self.MAX_GLOBAL_EP = params['MAX_GLOBAL_EP']

    def work(self, action_dict,env, otherplayers):
        global GLOBAL_RUNNING_R, GLOBAL_EP
        buffer_s, buffer_a, buffer_r = [], [], []
        while not self.COORD.should_stop() and GLOBAL_EP < self.MAX_GLOBAL_EP:
            infos, public, person_states, private_state, _ = env.init(self.params)
            for i in range(1,len(infos)):
                otherplayers[i-1].receive_info(infos[i])
            ep_r = 0
            while public[-1].is_terminal == False:
                turn = public[-1].turn

                if turn == 0:# A3C learner
                    s = np.zeros((14, 8, 1))
                    if (public[-1].param_dealer_id == 0):
                        for card in infos[0].public_state_history[-1].public_cards:
                            s[card.point_rank, card.suit_rank, 0] = 1
                        for card in infos[0].person_state_history[-1].hand_cards:
                            s[card.point_rank, card.suit_rank, 0] = 1
                    else:
                        for card in infos[0].public_state_history[-1].public_cards:
                            s[card.point_rank, card.suit_rank + 4, 0] = 1
                        for card in infos[0].person_state_history[-1].hand_cards:
                            s[card.point_rank, card.suit_rank + 4, 0] = 1
                    available_action = dict()
                    available_option = []
                    for action in list(infos[0].person_state_history[-1].available_actions.values()):
                        option = action.option
                        if option not in available_option:
                            available_option.append(option)
                            available_action[option] = action
                    a = self.AC.choose_action(s, available_option, action_dict)
                    action = available_action[a]
                    buffer_s.append(s)
                    buffer_a.append(action_dict[a])
                    buffer_r.append(0)
                    # print("action0", action.option)
                else:  # other players
                    action = otherplayers[turn-1].take_action()
                infos, public, persons, private, _ = env.forward(action)
                for i in range(1,len(infos)):
                    otherplayers[i-1].receive_info(infos[i])
            if (len(buffer_r) == 0):
                #a3c player is first hander and choose fold
                continue
            # print("score", public[-1].scores[0])
            buffer_r[-1] = public[-1].scores[0]
            ep_r += buffer_r[-1]
            v_s_ = 0  # terminal
            buffer_v_target = []
            for r in buffer_r[::-1]:  # reverse buffer r
                v_s_ = r + self.gamma * v_s_
                buffer_v_target.append(v_s_)
            buffer_v_target.reverse()

            buffer_s, buffer_a, buffer_v_target = np.stack(buffer_s, axis=0), np.array(buffer_a), np.vstack(buffer_v_target)
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

            print(
                self.name,
                "Ep:", GLOBAL_EP,
                "| Ep_r: %.3f" % GLOBAL_RUNNING_R[-1],
            )
            GLOBAL_EP += 1



class AbstractA3C(object):

    def __init__(self,
                 state_spec,
                 n_a,
                 params = dict()
                 ):

        self.params = params

        if 'MAX_GLOBAL_EP' not in params:
            self.params['MAX_GLOBAL_EP'] = 50000

        if 'GAMMA' not in params:
            self.params['GAMMA'] = 0.9

        if 'ENTROPY_BETA' not in params:
            self.params['ENTROPY_BETA']=0.001

        if 'LR_A' not in params:
            self.params['LR_A'] = 0.0001

        if 'LR_C' not in params:
            self.params['LR_C'] = 0.0001

        if 'MODEL_DIR' not in params:
            self.params['MODEL_DIR'] = './checkpoint/a3cmodel'

        if 'OUTPUT_GRAPH' not in params:
            self.params['OUTPUT_GRAPH'] = False

        if 'LOG_DIR' not in params:
            self.params['LOG_DIR'] = './log'

        self.graph = tf.Graph()
        with self.graph.as_default() as graph:
            self.sess = tf.Session()
            self.COORD = tf.train.Coordinator()
            with tf.device("/cpu:0"):
                self.GLOBAL_AC = ACNet('Global_Net', self.params, state_spec, n_a, self.sess)  # we only need its params
                self.workers = []
                N_WORKERS = multiprocessing.cpu_count()
                # Create worker
                for i in range(N_WORKERS):
                    i_name = 'W_%i' % i  # worker name
                    worker_net = ACNet(i_name, self.params, state_spec, n_a, self.sess, self.GLOBAL_AC)
                    self.workers.append(Worker(i_name, self.sess, self.COORD, worker_net, self.params))
            self.sess.run(tf.global_variables_initializer())
            self.saver = tf.train.Saver(max_to_keep=1)

    def train(self,action_dict):
        self.saver.save(self.sess, self.params['MODEL_DIR'])
        if self.params['OUTPUT_GRAPH']:
            if os.path.exists(self.params['LOG_DIR']):
                shutil.rmtree(self.params['LOG_DIR'])
            tf.summary.FileWriter(self.params['LOG_DIR'], self.sess.graph)

        with tf.variable_scope('A3CModel'):
            worker_threads = []
            for worker in self.workers:
                job = lambda: worker.work(action_dict,self.params['env'], self.params['otherplayers'])
                t = threading.Thread(target=job)
                t.start()
                worker_threads.append(t)
            self.COORD.join(worker_threads)

    def choose_action(self, s, available_action, action_dict):
        actions = dict()
        for work in self.workers:
            a = work.AC.choose_action(s, available_action, action_dict)
            if (a in actions.keys()):
                actions[a] += 1
            else:
                actions[a] = 1
        action_list = [[v[1], v[0]] for v in actions.items()]
        action_list.sort(key=lambda x: -x[0])
        return (action_list[0][1])

    def load_model(self,model_path='./checkpoint',model_name='a3cmodel'):
        self.saver = tf.train.import_meta_graph(model_path+"/"+model_name +".meta")
        self.saver.restore(self.sess, tf.train.latest_checkpoint(model_path))

