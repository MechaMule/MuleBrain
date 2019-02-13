from hcsr04sensor import sensor

if __name__ == '__main__':
    trig_pin = 17
    echo_pin = 27
    value = sensor.Measurement(trig_pin, echo_pin)
    while 1:    
        
        raw_measurement = value.raw_distance()

        metric_distance = value.distance_metric(raw_measurement)

        print("The Distance = {} centimeters".format(metric_distance*0.393701))
        input("Press enter to continue")
       
