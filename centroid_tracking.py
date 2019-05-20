from pyimagesearch.centroidtracker import CentroidTracker  
import cv2

def line(x, x1, y1, x2, y2):

	y = (float((y2-y1)/(x2-x1))*(x-x1))+y1

	return y

def Drawline(frame, x1, y1, x2, y2):

	return cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

ct = CentroidTracker(maxDisappeared=10, maxDistance=300)
trackableObjects = {}

while True:

	x1 = int(0)
	x2 = int(W)
	y1 = int(H//2)
	y2 = int(H//2)

	Drawline(result, x1, y1, x2, y2)

	objects = ct.update(box)

	for (objectID, centroid) in objects.items():
		to = trackableObjects.get(objectID, None)

		if to is None:
			to = TrackableObject(objectID, centroid)

		else:
			x = [u[0] for u in to.centroids]
			y = [c[1] for c in to.centroids]

			direction = centroid[1] - np.mean(y)
			to.centroids.append(centroid)

			last_x = x[-1]
			last_y = y[-1]
			now_x = centroid[0]
			now_y = centroid[1]

			line_last_y = line(last_x, x1, y1, x2, y2)
			line_now_y = line(now_x, x1, y1, x2, y2)

			if not to.counted:

				if (last_y - line_last_y) > 0 and  (now_y - line_now_y) <= 0:
					totalUp += 1
					to.counted = True

				elif (last_y - line_last_y) < 0 and  (now_y - line_now_y) >= 0:
					totalDown += 1
					to.counted = True

		trackableObjects[objectID] = to

		text = "ID {}".format(objectID)
		cv2.putText(result, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(result, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)


	info = [
		("up", totalUp),
		("Down", totalDown),
		]

	for (i, (k, v)) in enumerate(info):
		text = "{}: {}".format(k, v)
		cv2.putText(result, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
