import matplotlib.pyplot as plt

data = [[0 for i in range(7)] for j in range(6)]
## data from data.txt
data[5] = [1.1247600000000001e-08, 7.6509590000000001e-10, 9.5163069999999997e-10, 1.1471000000000001e-09, 1.3476e-09, 1.5590000000000001e-09, 1.7632000000000003e-09]
data[4] = [1.1150800000000001e-08, 6.7192039999999991e-10, 7.8810850000000002e-10, 9.4138129999999991e-10, 1.1040000000000001e-09, 1.2687e-09, 1.4321e-09]
data[3] = [1.1046600000000001e-08, 6.6988319999999995e-10, 6.3627089999999999e-10, 7.3798119999999994e-10, 8.5873350000000007e-10, 9.7301610000000001e-10, 1.0951000000000001e-09]
data[2] = [1.0941800000000002e-08, 1.0435000000000002e-09, 5.9408050000000004e-10, 5.7877340000000001e-10, 6.3154049999999992e-10, 7.0249019999999998e-10, 7.8134929999999998e-10]
data[1] = [1.0875500000000002e-08, 2.9544000000000005e-09, 1.4686000000000001e-09, 1.0007999999999999e-09, 8.1063179999999998e-10, 7.2856780000000002e-10, 6.9451089999999999e-10]
data[0] = [1.0805400000000002e-08, 1.0805400000000002e-08, 1.0805400000000002e-08, 1.0805400000000002e-08, 1.0805400000000002e-08, 1.0805400000000002e-08, 1.0805400000000002e-08]

min_result = []
for i in range(6):
    min_result.append(min(data[i]))

plt.plot(range(1,13,2),min_result)
plt.title('Delay of Different Inverter Numbers')
plt.xlabel('Number of inverters')
plt.ylabel('Delay(second)')
plt.grid()
plt.savefig("Proj4_inv_analysis.png")
plt.show()

plt.plot(range(1,8),data[0])
plt.plot(range(1,8),data[1])
plt.plot(range(1,8),data[2])
plt.plot(range(1,8),data[3])
plt.plot(range(1,8),data[4])
plt.plot(range(1,8),data[5])
plt.title('Delay of Different Fan with Respect to Number of Inverters')
plt.xlabel('Fan Ratio')
plt.ylabel('Delay(second)')
plt.grid()
plt.legend(['Inv # = 1', 'Inv # = 3', 'Inv # = 5', 'Inv # = 7', 'Inv # = 9', 'Inv # = 11'], loc='upper left')
plt.savefig("Proj4_fan_analysis.png")
plt.show()
