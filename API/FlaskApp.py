import flask
from flask import request, jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

@app.route('/')
def index():
    return '<h3>Timeslot API</h3>'

@app.route('/getTimeSlot', methods=['GET'])
def getData():
    bookingOpeningTime = 9
    bookingClosingTime = 17
    hourSplitAmount = 2
    timeSlotQty = bookingClosingTime - bookingOpeningTime
    bookingSlots = []
    index = 0

    try:
        for i in range(timeSlotQty):
            increment = HourSplitIncrement(hourSplitAmount)
            currentTimeSlotMinutes = 0

            for j in range(hourSplitAmount):
                bookingSlots.append(CreateTimeSlot(index,GetFormattedTime(bookingOpeningTime, currentTimeSlotMinutes), GetFormattedTime(bookingOpeningTime, currentTimeSlotMinutes + increment), "available"))
                currentTimeSlotMinutes = currentTimeSlotMinutes + increment
                index = index + 1
            bookingOpeningTime = bookingOpeningTime + 1

        return jsonify(dict({"Data":bookingSlots}))
    except:
        return jsonify(dict({"Data Error": "Error Geting time"}))


def HourSplitIncrement(hourSplitAmount):
    increment = 0
    if hourSplitAmount == 1:
        increment = 60
    elif hourSplitAmount == 2:
        increment = 30
    elif hourSplitAmount == 4:
        increment = 15
    else:
        increment = 60
    return increment

def CreateTimeSlot(slotId, startTime, endTime, bookingStatus):
    slot = dict({
        "slotId": slotId,
        "startTime": startTime,
        "endTime": endTime,
        "bookingStatus": bookingStatus,
    })
    return slot

def GetFormattedTime(hour, min):
    if min == 60:
        hour = hour + 1
        min = 0
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    if len(str(min)) == 1:
        min = "0" + str(min)
    return str(hour)+":"+str(min)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)