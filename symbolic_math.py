#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 17:46:20 2019

@author: emil
"""
import sympy as sp
import re
from numbafy import numbafy

# file = open('partials.txt', 'w')

g = sp.Symbol('g')
m, ix, iy, iz = sp.symbols(['m', 'ix', 'iy', 'iz'])
fx, fy, fz, mx, my, mz = sp.symbols(['fx', 'fy', 'fz', 'mx', 'my', 'mz'])
ft = sp.symbols('ft')

roll, pitch, yaw = sp.symbols(['roll', 'pitch', 'yaw'])
p, q, r = sp.symbols(['p', 'q', 'r'])
u, v, w = sp.symbols(['u', 'v', 'w'])
x, y, z = sp.symbols(['x', 'y', 'z'])

initials = {roll:0, pitch:0, yaw:0, p:0, q:0, r:0, u:0, v:0, w:0, x:0, y:0, z:0}

roll_d, pitch_d, yaw_d = sp.symbols(['roll_d', 'pitch_d', 'yaw_d'])
p_d, q_d, r_d = sp.symbols(['p_d', 'q_d', 'r_d'])
u_d, v_d, w_d = sp.symbols(['u_d', 'v_d', 'w_d'])
x_d, y_d, z_d = sp.symbols(['x_d', 'y_d', 'z_d'])


Rx, Ry, Rz, R = sp.symbols(['Rx', 'Ry', 'Rz', 'R'])

T = sp.symbols('T')

v, vb, omega, omegab = sp.symbols(['v', 'vb', 'omega', 'omegab'])

cos = sp.cos
sin = sp.sin
tan = sp.tan

X = sp.Matrix([[roll],[pitch],[yaw],
                  [p],[q],[r],
                  [u],[v],[w],
                  [x],[y],[z]])

U = sp.Matrix([[ft, mx, my, mz]]).T

Rx = sp.Matrix([[1,             0,          0],
                [0,     cos(roll), -sin(roll)],
                [0,     sin(roll), cos(roll)]])

Ry = sp.Matrix([[cos(pitch),    0, sin(pitch)],
                [0,             1,          1],
                [-sin(pitch),   0, cos(pitch)]])

Rz = sp.Matrix([[cos(yaw), -sin(yaw),    0],
                [sin(yaw),  cos(yaw),    0],
                [0,                0,    1]])


R = Rz * Ry * Rx

T = sp.Matrix([[1, sin(roll)*tan(pitch),  cos(roll)*tan(pitch)],
               [0,            cos(roll),            -sin(roll)],
               [0, sin(roll)/cos(pitch), cos(roll)/cos(pitch)]])


vb = sp.Matrix([[u, v, w]]).T
omegab = sp.Matrix([[p, q, r]]).T

v       = R*vb
omega   = T*omegab

x_d, y_d, z_d = v
roll_d, pitch_d, yaw_d = omega


fb = R.T*sp.Matrix([[0, 0, m*g]]).T - ft * sp.Matrix([[0, 0, 1]]).T
vb_d = fb/m - omegab.cross(vb)
u_d, v_d, w_d = vb_d

inertia = sp.diag(ix, iy, iz)
mb = sp.Matrix([[mx, my, mz]]).T
omegab_d = inertia.inv() * (mb - omegab.cross(inertia * omegab))
p_d, q_d, r_d = omegab_d

X_d = sp.Matrix([[roll_d],[pitch_d],[yaw_d],
                  [p_d],[q_d],[r_d],
                  [u_d],[v_d],[w_d],
                  [x_d],[y_d],[z_d]])

A = X_d.jacobian(X)













