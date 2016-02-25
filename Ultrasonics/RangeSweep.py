import time
from SR04_single import SR04_Single

class RangeSweep:
    def __init__(self):
        self.ranger1 = SR04_Single(17,27,0)
        self.ranger2 = SR04_Single(23,24,120)
        self.ranger3 = SR04_Single(10,9,-120)

    def fullRange(self):
        range_data = []
        #start each ranger slighty offset on time
        self.ranger1.start()
        time.sleep(0.05)
        self.ranger2.start()
        time.sleep(0.05)
        self.ranger3.start()
        
        #control the servo and update the angles
        time.sleep(0.5)
        #ranger1.setAngle(0)
        self.ranger1.stop()
        self.ranger2.stop()
        self.ranger3.stop()
        #wait for rangers to finish final reading
        time.sleep(0.1)
        range_data.extend(self.ranger1.getRangeData())
        range_data.extend(self.ranger2.getRangeData())
        range_data.extend(self.ranger3.getRangeData())
        self.ranger1.clearRangeData();
        self.ranger2.clearRangeData();
        self.ranger3.clearRangeData();

        return range_data

    def cleanup():
        self.ranger1.cleaup()
        self.ranger2.cleaup()
        self.ranger3.cleaup()


if __name__ == "__main__":
    print "setting up rangers"
    r = RangeSweep()
    time.sleep(3)
    print "reading..."
    data = r.fullRange()
    for i in range(0,len(data) - 1):
        print "Angle : " + str(data[i].angle)
        print "Distance:" + str(data[i].distance)
        
        
