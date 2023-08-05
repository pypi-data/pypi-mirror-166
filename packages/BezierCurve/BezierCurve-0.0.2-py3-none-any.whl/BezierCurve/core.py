import matplotlib.pyplot as plt
import numpy as np
from math import *
class BezierCurve:
	def __init__(self,points,weights,number):
		self.points = np.array(points);
		self.weights = np.array(weights);
		self.n = len(self.points)-1
		self.number = number
	def binomial_coefficient(self,n,k):
		return factorial(n)/(factorial(k)*factorial(n-k))
	def B(self,i,n,t):
		#bernstein_polynomials
		if i<0 or i>n:
			return 0
		binomial_coeff = self.binomial_coefficient(n,i)
		return binomial_coeff*(t**i)*((1-t)**(n-i));		
	def w(self,i,k,t):
		ret = 0
		n = self.n
		w = self.weights
		for j in range(0,k+1):
			if i+j >= n:
				ret +=self.B(j,k,t)*w[n]
			else:
				ret += self.B(j,k,t)*w[i+j]
		return ret;	
	def _lambda(self,i,t,w):
		ret = 0.0;
		n = self.n
		for j in range(0,i+1):
			for k in range(i+1,n+1):
				ret +=(k-j)*self.B(j,n,t)*self.B(k,n,t)*w[j]*w[k];
		ret /= ((1-t)*t*self.w(0,n,t,w)**2)
		return ret;
	def P(self,i,k,t):
		P_ = self.points;
		w_ = self.weights;
		num=0;
		den=0;		
		if k==0:
			return P_[i]
		for j in range(0,k+1):
			num+= self.B(j,k,t)*w_[i+j]*P_[i+j]
			den+= self.B(j,k,t)*w_[i+j]
		return num/den
	def P_prime(self,i,t):
		n =self.n
		P_ = np.array(self.points)
		w_ = np.array(self.weights)
		P_prime_val = n*(self.w(0,n-1,t)*self.w(1,n-1,t))/(self.w(0,n,t)**2)*(self.P(1,n-1,t)-self.P(0,n-1,t))
		return P_prime_val
	def P_two_prime(self,i,k,t):
		P_ = np.array(self.points)
		w = np.array(self.weights)
		n = self.n
		P_two_prime_val = n*(self.w(2,n-2,t)/(self.w(0,n,t)**3))*(2*n*self.w(0,n-1,t)**2-(n-1)*self.w(0,n-2,t)*self.w(0,n,t)-2*self.w(0,n-1,t)*self.w(0,n,t))*(self.P(2,n-2,t)-self.P(1,n-2,t))-n*(self.w(0,n-2,t)/(self.w(0,n,t)**3))*(2*n*self.w(1,n-1,t)**2-(n-1)*self.w(2,n-1,t)*self.w(0,n,t)-2*self.w(1,n-1,t)*self.w(0,n,t))*(self.P(1,n-2,t)-self.P(0,n-2,t))
		return P_two_prime_val			
	def get_bazier_curve(self):
		dt = 1/self.number
		n = self.n
		ret_P=[]
		ret_P_prime=[]	
		ret_P_two_prime=[]	
		for j in range(self.number):
			t= j/self.number;
			ret_P.append(self.P(0,n,t))
			ret_P_prime.append(self.P_prime(0,t))
			ret_P_two_prime.append(self.P_two_prime(0,n,t))
		return np.array(ret_P),np.array(ret_P_prime),np.array(ret_P_two_prime)		
