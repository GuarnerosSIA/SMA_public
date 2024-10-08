import numpy as np

class STA:
    
    def __init__(self,tau,l1, l2, w1=0.0, w2=0.0):
        self.tau = tau
        self.w1 = [w1]
        self.w2 = [w2]
        self.l1 = l1
        self.l2 = l2
    
    def derivative(self,variable):
        error = self.w1[-1]-variable
        w1_aux = self.tau*(self.w2[-1] - self.l1*(np.sqrt(np.abs(error)))*np.sign(error)) + self.w1[-1]
        w2_aux = self.tau*(-self.l2*np.sign(error)) + self.w2[-1]
        self.w1.append(w1_aux)
        self.w2.append(w2_aux)
        
        return w2_aux