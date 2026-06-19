import machine
import pyb
import time

adc=pyb.ADC(machine.Pin('Y4'))
servo= pyb.Servo(1)

x_data = []
y_data = []
print("===TRAINING PHASE===")
print("Move slider and press ENTER when ready")

training_angles = [90, 70, 50, 30, 10, 0]
for angle in training_angles:
    input("Set slider position then press ENTER...")
    x=adc.read()
    
    x_data.append(x)
    y_data.append(angle)
    
    print("ADC =", x, "Desired Angle =", angle)
print("\nTraining Data Collected")
print("x=", x_data)
print("y=", y_data)

n = len(x_data)

mean_x = sum(x_data)/n
mean_y = sum(y_data)/n

num=0
den=0

for i in range(n):
    num += (x_data[i] - mean_x) * (y_data[i] - mean_y)
    den += (x_data[i] - mean_x)**2

m = num/den
b = mean_y - m * mean_x

print("\n=== Training Model ===")
print("angle = m*x +b")
print("m =", m)
print("b =", b)

print("\n=== PREDICTION PHASE ===")

while True:
    x = adc.read()
    angle = m*x+b
    if angle<0:
        angle = 0
    
    if angle>90:
        angle=90
    servo.angle(int(angle))
    
    print("--------------------")
    print("ADC =", x)
    print("Predicted Angle =", int(angle))
    
    time.sleep(1)
