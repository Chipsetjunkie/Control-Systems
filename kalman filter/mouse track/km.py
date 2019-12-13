import numpy as np


class Kalman_Filter:
    def __init__(self,states,dt,a_x=0,a_y=0):
        self.State_Matrix = np.zeros((states,1))
        self.Estimated_Covariance = np.eye(states)
        self.Transition_Matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]])
        self.Process_Noise_Cov = np.eye(states)# Most important parameter since Estimated_Covariance is updated with this value
        self.Measurement_Noise_Cov = np.eye(2,2)
        self.Observation_Noise_Cov = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.Measure_State_Matrix = np.array([[0],[0],[0],[0]])
        self.Observation_Matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]])
        self.Control_Matrix = np.array([[0.5*dt,0],[0,0.5*dt],[dt,0],[0,dt]])
        self.Control_Vector = np.array([[a_x],[a_y]])


    def set_state(self,mat):
        mat = np.array(mat)
        self.State_Matrix = mat.reshape(self.State_Matrix.shape)

    def set_pro_cov(self,sigma_1,sigma_2,sigma_3,sigma_4):
        self.Estimated_Covariance = np.array([[sigma_1**2, 0,0,0,],
                                                [0,sigma_2**2,0,0],
                                                [0,0,sigma_3**2,0],
                                                [0,0,0,sigma_4**2]])
        ''''
        np.array([[sigma_1**2, sigma_1*sigma_2,sigma_1*sigma_3,sigma_1*sigma_4],
                                                [sigma_1*sigma_2,sigma_2**2,sigma_2*sigma_3, sigma_2*sigma_4],
                                                [sigma_1*sigma_3,sigma_2*sigma_3,sigma_3**2,sigma_4*sigma_3],
                                                [sigma_1*sigma_4,sigma_2*sigma_4,sigma_3*sigma_4,sigma_4**2]])

        '''

    def set_measure(self,mat):
        mat = np.array(mat)
        self.Measure_State_Matrix = mat.reshape(len(mat),1)


    def predict(self):
        self.State_Matrix = np.dot(self.Transition_Matrix,self.State_Matrix)+ np.dot(self.Control_Matrix,self.Control_Vector)
        self.Estimated_Covariance = np.dot(np.dot(self.Transition_Matrix,self.Estimated_Covariance),self.Transition_Matrix.T) + self.Process_Noise_Cov
        self.Estimated_Covariance = self.Estimated_Covariance*np.eye(4,4)


    def Update(self):

        Kalman_Gain =np.nan_to_num(np.dot(self.Estimated_Covariance ,self.Observation_Matrix)\
                    /(np.dot(np.dot(self.Estimated_Covariance,self.Observation_Matrix),self.Observation_Matrix.T)+self.Observation_Noise_Cov))

        print(self.Measure_State_Matrix)
        self.State_Matrix = self.State_Matrix+ np.dot(Kalman_Gain,(self.Measure_State_Matrix - np.dot(self.Observation_Matrix,self.State_Matrix)))
        self.Estimated_Covariance = self.Estimated_Covariance - np.dot(Kalman_Gain,np.dot(self.Observation_Matrix,self.Estimated_Covariance))
        return self.State_Matrix
