import cv2 
from pyzbar.pyzbar import decode
import numpy as np
import vg
import math

#video_capture1 = cv2.VideoCapture(0)
video_capture2 = cv2.VideoCapture(2)
#video_capture3 = cv2.VideoCapture(4)

a = 142
b = 142*1.4142
c = 142

h_1 = (a**2 - c**2)/b**2
h_2 = (a**2 + c**2)/b**2
h_3 = (b**2 - c**2)/b**2
h_4 = (b**2 - a**2)/b**2

while(True):

	#ret1, frame1 = video_capture1.read()
	ret2, frame2 = video_capture2.read()
	#ret3, frame3 = video_capture3.read()

	#code1 = decode(frame1)
	code2 = decode(frame2)
	#code3 = decode(frame3)		

	#for qrcode1 in code1:
    	#points = np.array(code1[0].polygon, np.int32)
		#cam_1_p_1 = points[0,:]
		#cam_1_p_2 = points[1,:]
		#cam_1_p_3 = points[2,:]
		#cam_1_p_4 = points[3,:]
    	#data_1 = qrcode1.data.decode("utf-8")
		#cam_1_p_1 = np.transpose([np.append(np.transpose(cam_1_p_1), [1] ,axis = 0)])
		#cam_1_p_2 = np.transpose([np.append(np.transpose(cam_1_p_2), [1] ,axis = 0)])
		#cam_1_p_3 = np.transpose([np.append(np.transpose(cam_1_p_3), [1] ,axis = 0)])
		#cam_1_p_4 = np.transpose([np.append(np.transpose(cam_1_p_4), [1] ,axis = 0)])
		#cam_cal_1 = np.array([[706.0479, 0, 326.7941], [0, 710.3787, 187.7707], [0, 0,1.0000]])
		#frame_1_p_1 = np.dot(np.linalg.inv(cam_cal_1), cam_1_p_1)
		#frame_1_p_2 = np.dot(np.linalg.inv(cam_cal_1), cam_1_p_2)
		#frame_1_p_3 = np.dot(np.linalg.inv(cam_cal_1), cam_1_p_3)
		#frame_1_p_4 = np.dot(np.linalg.inv(cam_cal_1), cam_1_p_4)
		#cam_1_alpha = vg.angle(np.transpose(frame_1_p_2), np.transpose(frame_1_p_3))
		#cam_1_beta = vg.angle(np.transpose(frame_1_p_3), np.transpose(frame_1_p_1))
		#cam_1_gama = vg.angle(np.transpose(frame_1_p_2), np.transpose(frame_1_p_1))

	
	for qrcode2 in code2:
		points = np.array(code2[0].polygon, np.int32)
		cam_2_p_1 = points[0,:]
		cam_2_p_2 = points[1,:]
		cam_2_p_3 = points[2,:]
		cam_2_p_4 = points[3,:]

		data_2 = qrcode2.data.decode("utf-8")

		cam_2_p_1 = np.transpose([np.append(np.transpose(cam_2_p_1), [1] ,axis = 0)])
		cam_2_p_2 = np.transpose([np.append(np.transpose(cam_2_p_2), [1] ,axis = 0)])
		cam_2_p_3 = np.transpose([np.append(np.transpose(cam_2_p_3), [1] ,axis = 0)])
		cam_2_p_4 = np.transpose([np.append(np.transpose(cam_2_p_4), [1] ,axis = 0)])
		cam_cal_2 = np.array([[715.4365, 0, 347.2345], [0, 710.3787, 187.7707], [0, 0,1.0000]])

		frame_2_p_1 = np.dot(np.linalg.inv(cam_cal_2), cam_2_p_1)
		print(frame_2_p_1)
		frame_2_p_2 = np.dot(np.linalg.inv(cam_cal_2), cam_2_p_2)
		frame_2_p_3 = np.dot(np.linalg.inv(cam_cal_2), cam_2_p_3)
		frame_2_p_4 = np.dot(np.linalg.inv(cam_cal_2), cam_2_p_4)

		cam_2_alpha = vg.angle(np.transpose(frame_2_p_2), np.transpose(frame_2_p_3))
		cam_2_beta = vg.angle(np.transpose(frame_2_p_3), np.transpose(frame_2_p_1))
		cam_2_gama = vg.angle(np.transpose(frame_2_p_2), np.transpose(frame_2_p_1))

		Cam_2_A0 = (1 + h_1)**2 - (4*a**2)/(b**2) * (math.cos(cam_2_gama))**2
		Cam_2_A1 = 4*(-h_1*(1+h_1)*math.cos(cam_2_beta) + 2 * a**2/b**2 * (math.cos(cam_2_gama)**2 * math.cos(cam_2_beta)) + (-1 +h_2) * math.cos(cam_2_alpha)*math.cos(cam_2_gama))
		Cam_2_A2 = 2*(h_1**2-1+2*h_1**2*(math.cos(cam_2_beta))**2+ 2*h_3*(math.cos(cam_2_alpha))**2- 4*h_2*math.cos(cam_2_alpha)*math.cos(cam_2_beta)*math.cos(cam_2_gama)+2*h_4*(math.cos(cam_2_gama))**2)
		Cam_2_A3 = 4*(h_1*(1-h_1)*math.cos(cam_2_beta)- (1-h_2)*math.cos(cam_2_alpha)*math.cos(cam_2_gama)+ 2*((c**2)/(b**2))*(math.cos(cam_2_alpha))**2*math.cos(cam_2_beta))
		Cam_2_A4 = (h_1 - 1)**2 - (4*c**2/b**2)*(math.cos(cam_2_alpha))**2


		Cam_2_K = np.array([[0, 0, 0, (-Cam_2_A4/Cam_2_A0)], [1, 0, 0, (-Cam_2_A3/Cam_2_A0)], [0, 1, 0, (-Cam_2_A2/Cam_2_A0)],[0, 0, 1, (-Cam_2_A1/Cam_2_A0)],])
		Cam_2_v, v = np.linalg.eig(Cam_2_K)
		
		Cam_2_v = [Cam_2_v[0].real, Cam_2_v[1].real, Cam_2_v[2].real, Cam_2_v[3].real]
		Cam_2_v_n = np.array(Cam_2_v)
		Cam_2_u_n = ((-1 + h_1) * Cam_2_v_n **2  - 2 * h_1 * math.cos(cam_2_beta)*Cam_2_v_n + 1 + h_1)/(2 * (math.cos(cam_2_gama)- Cam_2_v_n * math.cos(cam_2_alpha)))
		
		cam2_s1 = b**2/(1 + Cam_2_v_n**2 - 2 * Cam_2_v_n * math.cos(cam_2_beta))
		cam2_s2 = Cam_2_u_n*cam2_s1
		cam2_s3 = Cam_2_v_n*cam2_s1

		print("s1 :", cam2_s1)
		print("s2 :", cam2_s2)
		print("s3 :", cam2_s3)


	#for qrcode1 in code1:
    	#points = np.array(code1[0].polygon, np.int32)
		#cam_3_p_1 = points[0,:]
		#cam_3_p_2 = points[1,:]
		#cam_3_p_3 = points[2,:]
		#cam_3_p_4 = points[3,:]
    	#data_3 = qrcode1.data.decode("utf-8")
		#cam_3_p_1 = np.transpose([np.append(np.transpose(cam_3_p_1), [1] ,axis = 0)])
		#cam_3_p_2 = np.transpose([np.append(np.transpose(cam_3_p_2), [1] ,axis = 0)])
		#cam_3_p_3 = np.transpose([np.append(np.transpose(cam_3_p_3), [1] ,axis = 0)])
		#cam_3_p_4 = np.transpose([np.append(np.transpose(cam_3_p_4), [1] ,axis = 0)])
		#cam_cal_3 = np.array([[706.0479, 0, 326.7941], [0, 710.3787, 187.7707], [0, 0,1.0000]])
		#frame_3_p_1 = np.dot(np.linalg.inv(cam_cal_3), cam_3_p_1)
		#frame_3_p_2 = np.dot(np.linalg.inv(cam_cal_3), cam_3_p_2)
		#frame_3_p_3 = np.dot(np.linalg.inv(cam_cal_3), cam_3_p_3)
		#frame_3_p_4 = np.dot(np.linalg.inv(cam_cal_3), cam_3_p_4)
		#cam_3_alpha = vg.angle(np.transpose(frame_3_p_2), np.transpose(frame_3_p_3))
		#cam_3_beta = vg.angle(np.transpose(frame_3_p_3), np.transpose(frame_3_p_1))
		#cam_3_gama = vg.angle(np.transpose(frame_3_p_2), np.transpose(frame_3_p_1))

	cv2.imshow("Frame2",frame2)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#video_capture1.release()
video_capture2.release()
#video_capture3.release()
cv2.destroyAllWindows()

